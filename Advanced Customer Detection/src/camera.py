import cv2
import pygame
import numpy as np
from datetime import datetime
from typing import Tuple, List, Optional, Deque
from numpy.typing import NDArray
import sys
from pathlib import Path
from collections import deque
import time

# Src klasörünü Python path'ine ekle
sys.path.append(str(Path(__file__).parent.parent))

from src.config import config
from src.logger import log_customer_detection, log_error, log_startup, log_shutdown
from src.database import get_db
from src.models import CustomerDetection

class FrameProcessor:
    """Görüntü işleme sınıfı."""
    
    def __init__(self):
        # Arka plan çıkarıcı - daha az hassas
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=1000,  # Daha uzun geçmiş
            varThreshold=32,  # Daha yüksek eşik değeri
            detectShadows=False  # Gölgeleri yok say
        )
        
        # Son tespitleri tutan kuyruk
        self.recent_detections: Deque[int] = deque(maxlen=10)
        self.last_detection_time = time.time()
        
        # Minimum boyut kontrolü için parametreler
        self.min_width = 60  # minimum genişlik
        self.min_height = 100  # minimum yükseklik
    
    def process_frame(self, frame: NDArray) -> Tuple[NDArray, NDArray, NDArray]:
        """Görüntüyü işle."""
        # Görüntüyü küçült (gürültüyü azaltır)
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fg_mask = self.bg_subtractor.apply(frame)
        
        # Gürültü temizleme
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        
        # Pygame için görüntüyü hazırla
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rotated_frame = np.rot90(rgb_frame)
        
        return gray, fg_mask, rotated_frame
    
    def detect_motion(self, mask: NDArray) -> List:
        """Hareket algıla ve konturları bul."""
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        valid_contours = []
        for cnt in contours:
            # Alan kontrolü
            area = cv2.contourArea(cnt)
            if area < config.detection.min_area:
                continue
                
            # Boyut kontrolü
            x, y, w, h = cv2.boundingRect(cnt)
            if w < self.min_width or h < self.min_height:
                continue
                
            # Aspect ratio kontrolü (insan şekline yakın olmalı)
            aspect_ratio = float(w) / h
            if not (0.3 <= aspect_ratio <= 0.8):
                continue
                
            valid_contours.append(cnt)
        
        return valid_contours
    
    def get_stable_count(self, current_count: int) -> int:
        """Stabil müşteri sayısını hesapla."""
        current_time = time.time()
        
        # Son tespiti ekle
        self.recent_detections.append(current_count)
        
        # Eğer yeterli süre geçmediyse önceki sayıyı kullan
        if current_time - self.last_detection_time < 1.0:  # 1 saniye bekle
            if len(self.recent_detections) > 0:
                return int(np.median(list(self.recent_detections)))
            return 0
            
        # Medyan filtreleme
        stable_count = int(np.median(list(self.recent_detections)))
        
        # Zamanı güncelle
        self.last_detection_time = current_time
        
        return stable_count
    
    @staticmethod
    def draw_detections(frame: NDArray, contours: List) -> None:
        """Tespit edilen hareketleri çerçeve içine al."""
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # Yeşil dikdörtgen çiz
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Merkez nokta çiz
            center = (x + w//2, y + h//2)
            cv2.circle(frame, center, 4, (0, 0, 255), -1)

class CustomerDetector:
    """Müşteri tespit sistemi."""
    
    def __init__(self):
        """Müşteri tespit sistemi başlatıcı."""
        config.validate()
        self._init_pygame()
        self._init_camera()
        self.frame_processor = FrameProcessor()
        self.db = next(get_db())
        self.last_save_time = time.time()
        log_startup()
    
    def _init_pygame(self) -> None:
        """Pygame'i başlat."""
        pygame.init()
        self.screen = pygame.display.set_mode((config.camera.width, config.camera.height))
        pygame.display.set_caption("Müşteri Tespit Sistemi")
        
        pygame.mixer.init()
        pygame.mixer.music.load(str(config.sound_file))
    
    def _init_camera(self) -> None:
        """Kamerayı başlat."""
        self.cap = cv2.VideoCapture(config.camera.id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.camera.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.camera.height)
        # Kamera ayarlarını optimize et
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    
    def play_alert(self) -> None:
        """Uyarı sesini çal."""
        current_time = time.time()
        if not pygame.mixer.music.get_busy() and current_time - self.last_save_time > 2.0:
            pygame.mixer.music.set_volume(config.sound.volume)
            pygame.mixer.music.play()
    
    def save_detection(self, count: int, confidence: Optional[float] = None) -> None:
        """Tespiti veritabanına kaydet."""
        current_time = time.time()
        # En az 2 saniye ara ile kaydet
        if current_time - self.last_save_time > 2.0 and count > 0:
            detection = CustomerDetection(
                timestamp=datetime.now(),
                customer_count=count,
                confidence_score=confidence,
                detection_area="main_entrance"
            )
            self.db.add(detection)
            self.db.commit()
            self.last_save_time = current_time
    
    def display_stats(self, count: int) -> None:
        """İstatistikleri ekranda göster."""
        font = pygame.font.Font(None, 36)
        text = font.render(f'Müşteri Sayısı: {count}', True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
    
    def process_frame(self) -> Tuple[bool, Optional[NDArray]]:
        """Kameradan görüntü al ve işle."""
        ret, frame = self.cap.read()
        if not ret:
            log_error(Exception("Kameradan görüntü alınamadı"))
            return False, None
        return True, frame
    
    def run(self) -> None:
        """Ana döngü."""
        try:
            running = True
            while running:
                ret, frame = self.process_frame()
                if not ret:
                    break
                
                # Görüntüyü işle
                gray, fg_mask, pygame_frame = self.frame_processor.process_frame(frame)
                contours = self.frame_processor.detect_motion(fg_mask)
                raw_count = len(contours)
                
                # Stabil sayıyı al
                stable_count = self.frame_processor.get_stable_count(raw_count)
                
                if stable_count > 0:
                    self.frame_processor.draw_detections(frame, contours)
                    self.play_alert()
                    self.save_detection(stable_count)
                    log_customer_detection(stable_count)
                
                # Ekranı güncelle
                self.screen.blit(pygame.surfarray.make_surface(pygame_frame), (0, 0))
                self.display_stats(stable_count)
                pygame.display.update()
                
                # Çıkış kontrolü
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                
        except Exception as e:
            log_error(e)
            raise
        
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """Kaynakları temizle."""
        self.cap.release()
        self.db.close()
        pygame.quit()
        log_shutdown()

def main() -> None:
    """Uygulamayı başlat."""
    detector = CustomerDetector()
    detector.run()

if __name__ == '__main__':
    main()
