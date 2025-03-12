from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass
import os

# .env dosyasını yükle
load_dotenv()

@dataclass
class CameraConfig:
    """Kamera ayarları."""
    id: int = int(os.getenv("CAMERA_ID", 0))
    width: int = int(os.getenv("FRAME_WIDTH", 640))
    height: int = int(os.getenv("FRAME_HEIGHT", 480))

@dataclass
class DetectionConfig:
    """Tespit ayarları."""
    interval: float = float(os.getenv("DETECTION_INTERVAL", 1.0))
    min_confidence: float = float(os.getenv("MIN_CONFIDENCE", 0.5))
    min_area: int = int(os.getenv("MIN_AREA", 500))

@dataclass
class SoundConfig:
    """Ses ayarları."""
    volume: float = float(os.getenv("SOUND_VOLUME", 1.0))

class AppConfig:
    """Uygulama konfigürasyonu."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.camera = CameraConfig()
        self.detection = DetectionConfig()
        self.sound = SoundConfig()
        
        # Dosya yolları
        self.sound_file = self.base_dir / "ses.mp3"
        self.db_path = self.base_dir / "database" / "customer_data.db"
        self.log_path = self.base_dir / "logs" / "app.log"
    
    def validate(self) -> None:
        """Konfigürasyon değerlerini doğrula."""
        assert self.camera.id >= 0, "Kamera ID negatif olamaz"
        assert 0 < self.camera.width <= 1920, "Geçersiz frame genişliği"
        assert 0 < self.camera.height <= 1080, "Geçersiz frame yüksekliği"
        assert 0 < self.detection.interval <= 10, "Geçersiz tespit aralığı"
        assert 0 <= self.detection.min_confidence <= 1, "Güven değeri 0-1 arasında olmalı"
        assert self.detection.min_area > 0, "Minimum alan pozitif olmalı"
        assert 0 <= self.sound.volume <= 1, "Ses seviyesi 0-1 arasında olmalı"
        assert self.sound_file.exists(), "Ses dosyası bulunamadı"

# Singleton instance
config = AppConfig() 