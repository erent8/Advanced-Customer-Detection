#!/usr/bin/env python3
"""
Kütüphane test scripti - tüm gereksinimlerin çalışıp çalışmadığını kontrol eder
"""

import sys

def test_dependencies():
    """Tüm bağımlılıkları test et"""
    print("🔍 Kütüphane testleri başlatılıyor...")
    print(f"Python sürümü: {sys.version}")
    print("-" * 50)
    
    failed_imports = []
    
    # Temel kütüphaneler
    test_packages = [
        ("cv2", "OpenCV"),
        ("numpy", "NumPy"), 
        ("PIL", "Pillow"),
        ("pandas", "Pandas"),
        ("matplotlib", "Matplotlib")
    ]
    
    # AI/ML kütüphaneleri
    ai_packages = [
        ("ultralytics", "YOLOv8"),
        ("torch", "PyTorch"),
        ("torchvision", "TorchVision")
    ]
    
    # Temel testler
    for package, name in test_packages:
        try:
            __import__(package)
            print(f"✅ {name} - OK")
        except ImportError as e:
            print(f"❌ {name} - HATA: {e}")
            failed_imports.append(name)
    
    # AI testleri
    print("\n🧠 AI/ML Kütüphane Testleri:")
    for package, name in ai_packages:
        try:
            if package == "ultralytics":
                from ultralytics import YOLO
                print(f"✅ {name} - OK")
            else:
                __import__(package)
                print(f"✅ {name} - OK")
        except ImportError as e:
            print(f"❌ {name} - HATA: {e}")
            failed_imports.append(name)
    
    # Opsiyonel kütüphaneler
    print("\n🔧 Opsiyonel Kütüphaneler:")
    optional_packages = [
        ("dlib", "Dlib (Yüz Tanıma)"),
        ("face_recognition", "Face Recognition")
    ]
    
    for package, name in optional_packages:
        try:
            __import__(package)
            print(f"✅ {name} - OK")
        except ImportError:
            print(f"⚠️  {name} - Yüklenmemiş (normal - sistem bu kütüphane olmadan da çalışır)")
    
    # Kamera testi
    print("\n📹 Kamera Testi:")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("✅ Kamera - OK")
            else:
                print("⚠️  Kamera açık ama görüntü alınamıyor")
            cap.release()
        else:
            print("⚠️  Kamera bulunamadı (normal - USB kamera bağlı değilse)")
    except Exception as e:
        print(f"❌ Kamera testi - HATA: {e}")
    
    # Sonuç
    print("\n" + "=" * 50)
    if failed_imports:
        print(f"❌ {len(failed_imports)} kütüphane eksik: {', '.join(failed_imports)}")
        print("\n🔧 Çözüm:")
        print("pip install -r requirements.txt")
        return False
    else:
        print("🎉 Tüm kütüphaneler başarıyla yüklendi!")
        print("✅ Sistem çalıştırılmaya hazır!")
        return True

if __name__ == "__main__":
    success = test_dependencies()
    if success:
        print("\n▶️  Sistemi başlatmak için:")
        print("python main.py")
    else:
        print("\n⚠️  Önce eksik kütüphaneleri yükleyin")
    
    input("\nDevam etmek için Enter'a basın...") 