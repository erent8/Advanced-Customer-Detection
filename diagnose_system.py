#!/usr/bin/env python3
"""
Sistem tanı scripti - sorunları tespit et
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def diagnose_system():
    """Sistem tanısı yap"""
    print("🔍 Sistem tanısı başlatılıyor...\n")
    
    issues = []
    
    # 1. Kütüphane kontrolü
    print("📚 Kütüphane Kontrolü:")
    try:
        import cv2
        print(f"✅ OpenCV: {cv2.__version__}")
    except ImportError as e:
        issues.append("OpenCV bulunamadı")
        print(f"❌ OpenCV: {e}")
    
    try:
        from ultralytics import YOLO
        print("✅ YOLOv8: OK")
        
        # Model test
        try:
            model = YOLO('yolov8n.pt')
            print("✅ YOLOv8 model yüklendi")
        except Exception as e:
            issues.append(f"YOLOv8 model yüklenemedi: {e}")
            print(f"❌ YOLOv8 model hatası: {e}")
            
    except ImportError as e:
        issues.append("YOLOv8 bulunamadı")
        print(f"❌ YOLOv8: {e}")
    
    # 2. Model dosyası kontrolü
    print("\n🤖 Model Kontrolü:")
    if os.path.exists("yolov8n.pt"):
        file_size = os.path.getsize("yolov8n.pt") / (1024*1024)  # MB
        print(f"✅ yolov8n.pt bulundu ({file_size:.1f} MB)")
    else:
        issues.append("yolov8n.pt model dosyası eksik")
        print("❌ yolov8n.pt bulunamadı")
    
    # 3. Kamera kontrolü
    print("\n📹 Kamera Kontrolü:")
    try:
        import cv2
        
        # Farklı kamera indekslerini test et
        for camera_idx in [0, 1, 2]:
            cap = cv2.VideoCapture(camera_idx)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    height, width = frame.shape[:2]
                    print(f"✅ Kamera {camera_idx}: {width}x{height}")
                    cap.release()
                    break
                else:
                    print(f"⚠️  Kamera {camera_idx}: Açık ama görüntü yok")
                cap.release()
            else:
                if camera_idx == 0:
                    print(f"❌ Kamera {camera_idx}: Açılamıyor")
        else:
            issues.append("Hiçbir kamera bulunamadı")
            print("❌ Hiçbir kamera çalışmıyor")
            
    except Exception as e:
        issues.append(f"Kamera testi hatası: {e}")
        print(f"❌ Kamera testi hatası: {e}")
    
    # 4. Database kontrolü
    print("\n💾 Database Kontrolü:")
    try:
        from src.models.database import db_manager
        if os.path.exists("data/musteri_analiz.db"):
            db_size = os.path.getsize("data/musteri_analiz.db") / 1024  # KB
            print(f"✅ Database dosyası mevcut ({db_size:.1f} KB)")
        else:
            print("⚠️  Database dosyası yok (ilk çalıştırmada oluşturulacak)")
            
        # Database bağlantı testi
        stats = db_manager.get_today_stats()
        print(f"✅ Database bağlantısı OK - Bugün: {stats.get('total_visitors', 0)} ziyaretçi")
        
    except Exception as e:
        issues.append(f"Database hatası: {e}")
        print(f"❌ Database hatası: {e}")
    
    # 5. Log kontrolü
    print("\n📝 Log Kontrolü:")
    if os.path.exists("logs/"):
        print("✅ Log klasörü mevcut")
        log_files = [f for f in os.listdir("logs/") if f.endswith('.log')]
        print(f"📄 {len(log_files)} log dosyası bulundu")
        
        # Son hataları kontrol et
        if os.path.exists("logs/errors.log"):
            with open("logs/errors.log", 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip():
                    print("⚠️  Error log'da hatalar var")
                else:
                    print("✅ Error log temiz")
    else:
        print("⚠️  Log klasörü yok")
    
    # 6. Threading test
    print("\n🧵 Threading Testi:")
    try:
        import threading
        import time
        
        test_result = []
        
        def test_thread():
            test_result.append("OK")
        
        thread = threading.Thread(target=test_thread)
        thread.start()
        thread.join(timeout=1)
        
        if test_result:
            print("✅ Threading çalışıyor")
        else:
            issues.append("Threading sorunu")
            print("❌ Threading sorunu")
            
    except Exception as e:
        issues.append(f"Threading hatası: {e}")
        print(f"❌ Threading hatası: {e}")
    
    # Sonuç
    print("\n" + "="*50)
    if issues:
        print(f"⚠️  {len(issues)} sorun tespit edildi:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        
        print("\n🔧 Önerilen çözümler:")
        print("1. pip install -r requirements_minimal.txt")
        print("2. Kamera bağlantısını kontrol edin")
        print("3. Kamera indeksini değiştirin (settings.py -> CAMERA_INDEX = 1)")
        print("4. YOLOv8 modelini indirin: python -c \"from ultralytics import YOLO; YOLO('yolov8n.pt')\"")
        print("5. Sanal ortamı yeniden oluşturun: .\\quick_setup.ps1")
        
        return False
    else:
        print("🎉 Sistem hazır - sorun tespit edilmedi!")
        return True

if __name__ == "__main__":
    diagnose_system() 