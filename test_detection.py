#!/usr/bin/env python3
"""
Tespit sistemi manuel test scripti
"""

import cv2
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.core.camera import CameraManager
from src.core.detector import HumanDetector
from src.core.visitor_tracker import visitor_tracker
from datetime import datetime

def test_detection_system():
    """Tespit sistemini test et"""
    print("🔍 Tespit sistemi testi başlatılıyor...")
    
    # Kamera ve detector başlat
    camera = CameraManager()
    detector = HumanDetector()
    
    # Kamerayı başlat
    if not camera.initialize_camera():
        print("❌ Kamera başlatılamadı!")
        return False
    
    # Detector'ı başlat
    if not detector.initialize():
        print("❌ YOLOv8 modeli yüklenemedi!")
        return False
    
    print("✅ Kamera ve model hazır - 'q' tuşuna basarak çıkış yapın")
    
    # Kamera yakalamayı başlat
    camera.start_capture()
    
    try:
        frame_count = 0
        while True:
            # Frame al
            frame = camera.get_current_frame()
            if frame is None:
                continue
            
            frame_count += 1
            
            # Tespit yap
            detections, processed_frame = detector.detect_humans(frame, draw_boxes=True)
            
            # Sonuçları göster
            if detections:
                print(f"🎯 Frame {frame_count}: {len(detections)} kişi tespit edildi!")
                
                # Visitor tracker'a gönder
                result = visitor_tracker.process_detections(detections, datetime.now())
                print(f"👥 Yeni ziyaretçi: {result['new_visitors']}")
                print(f"📊 Toplam bugün: {result['current_stats']['total_today']}")
            
            # Görüntüyü göster
            cv2.imshow("Test - Tespit Sistemi", processed_frame)
            
            # Çıkış kontrolü
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\n⏹️  Test durduruldu")
    
    finally:
        camera.stop_capture()
        detector.cleanup()
        cv2.destroyAllWindows()
    
    print("✅ Test tamamlandı")
    return True

if __name__ == "__main__":
    test_detection_system() 