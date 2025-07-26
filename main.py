#!/usr/bin/env python3
"""
OpenCV Müşteri Analiz Sistemi - Ana Başlangıç Dosyası
Bu dosya uygulamanın ana giriş noktasıdır.

Kullanım:
    python main.py

Gereksinimler:
    - Python 3.8+
    - requirements.txt dosyasındaki tüm kütüphaneler
"""

import sys
import os
import traceback
from pathlib import Path

# Proje kök dizinini Python path'ine ekle
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    # Konfigürasyonu yükle ve gerekli klasörleri oluştur
    from src.config.settings import SETTINGS
    
    # Log sistemini başlat
    from src.utils.logger import log_manager, get_logger
    
    # Ana pencereyi import et
    from src.ui.main_window import MainWindow
    
except ImportError as e:
    print(f"❌ Kütüphane import hatası: {e}")
    print("\n🔧 Çözüm önerileri:")
    print("1. Minimal kütüphaneleri yükleyin:")
    print("   pip install -r requirements_minimal.txt")
    print("\n2. Tam kütüphaneleri yükleyin:")
    print("   pip install -r requirements.txt")
    print("\n3. Python sürümünüzün 3.8+ olduğundan emin olun:")
    print("   python --version")
    print("\n4. Sanal ortamı etkinleştirdiğinizden emin olun")
    print("\n5. Otomatik kurulum kullanın:")
    print("   .\\quick_setup.ps1  (PowerShell)")
    print("   quick_setup.bat    (Command Prompt)")
    sys.exit(1)

def check_dependencies():
    """
    Sistem gereksinimlerini kontrol et.
    
    Returns:
        bool: Temel gereksinimler karşılanırsa True
    """
    logger = get_logger("startup")
    logger.info("Sistem gereksinimleri kontrol ediliyor...")
    
    missing_critical_deps = []
    optional_missing = []
    
    # TEMEL KÜTÜPHANELER (Sistemin çalışması için gerekli)
    
    # OpenCV kontrolü (kritik)
    try:
        import cv2
        logger.info(f"✅ OpenCV bulundu: {cv2.__version__}")
    except ImportError:
        missing_critical_deps.append("opencv-python")
        logger.error("❌ OpenCV bulunamadı - GEREKLI")
    
    # NumPy kontrolü (kritik)
    try:
        import numpy as np
        logger.info(f"✅ NumPy bulundu: {np.__version__}")
    except ImportError:
        missing_critical_deps.append("numpy")
        logger.error("❌ NumPy bulunamadı - GEREKLI")
    
    # PIL/Pillow kontrolü (kritik)
    try:
        from PIL import Image
        logger.info("✅ Pillow bulundu")
    except ImportError:
        missing_critical_deps.append("Pillow")
        logger.error("❌ Pillow bulunamadı - GEREKLI")
    
    # YAPAY ZEKA KÜTÜPHANELERI (Opsiyonel ama önemli)
    
    # YOLOv8 kontrolü (opsiyonel - sistem çalışır ama tespit olmaz)
    try:
        import ultralytics
        logger.info("✅ YOLOv8 (ultralytics) bulundu")
        SETTINGS.YOLO_ENABLED = True
    except ImportError:
        optional_missing.append("ultralytics")
        logger.warning("⚠️  YOLOv8 bulunamadı - İnsan tespiti devre dışı")
        SETTINGS.YOLO_ENABLED = False
    
    # PyTorch kontrolü (opsiyonel)
    try:
        import torch
        logger.info(f"✅ PyTorch bulundu: {torch.__version__}")
    except ImportError:
        optional_missing.append("torch")
        logger.warning("⚠️  PyTorch bulunamadı")
    
    # VERİ ANALİZİ KÜTÜPHANELERI (Opsiyonel)
    
    # Pandas kontrolü (opsiyonel)
    try:
        import pandas as pd
        logger.info(f"✅ Pandas bulundu: {pd.__version__}")
    except ImportError:
        optional_missing.append("pandas")
        logger.warning("⚠️  Pandas bulunamadı - Veri analizi sınırlı")
    
    # Matplotlib kontrolü (opsiyonel)
    try:
        import matplotlib
        logger.info("✅ Matplotlib bulundu")
    except ImportError:
        optional_missing.append("matplotlib")
        logger.warning("⚠️  Matplotlib bulunamadı - Grafik özelliği devre dışı")
    
    # YÜZ TANIMA KÜTÜPHANELERI (Tamamen opsiyonel)
    
    # Dlib kontrolü (tamamen opsiyonel)
    try:
        import dlib
        logger.info("✅ Dlib bulundu (yüz tanıma etkin)")
        SETTINGS.FACE_RECOGNITION_ENABLED = True
    except ImportError:
        logger.warning("⚠️  Dlib bulunamadı (yüz tanıma devre dışı - normal)")
        SETTINGS.FACE_RECOGNITION_ENABLED = False
    
    # Face Recognition kontrolü (tamamen opsiyonel)
    try:
        import face_recognition
        logger.info("✅ Face Recognition bulundu")
    except ImportError:
        logger.warning("⚠️  Face Recognition bulunamadı (normal)")
    
    # SONUÇ DEĞERLENDİRMESİ
    
    if missing_critical_deps:
        logger.error(f"❌ KRİTİK eksik kütüphaneler: {', '.join(missing_critical_deps)}")
        logger.error("Bu kütüphaneler olmadan sistem çalışmaz!")
        logger.error("Çözüm:")
        logger.error("  pip install -r requirements_minimal.txt")
        logger.error("  veya")
        logger.error(f"  pip install {' '.join(missing_critical_deps)}")
        return False
    
    if optional_missing:
        logger.warning(f"⚠️  Opsiyonel eksik kütüphaneler: {', '.join(optional_missing)}")
        logger.warning("Sistem çalışacak ama bazı özellikler sınırlı olabilir")
    
    logger.info("✅ Kritik gereksinimler karşılandı - sistem çalışabilir")
    return True

def check_camera():
    """
    Kamera erişimini kontrol et.
    
    Returns:
        bool: Kamera erişilebilirse True
    """
    logger = get_logger("startup")
    
    try:
        import cv2
        
        # Kamerayı test et
        logger.info(f"Kamera testi yapılıyor (Index: {SETTINGS.CAMERA_INDEX})...")
        cap = cv2.VideoCapture(SETTINGS.CAMERA_INDEX)
        
        if not cap.isOpened():
            logger.warning(f"❌ Kamera {SETTINGS.CAMERA_INDEX} açılamadı")
            
            # Alternatif kameraları dene
            for i in range(3):
                logger.info(f"Alternatif kamera deneniyor: {i}")
                test_cap = cv2.VideoCapture(i)
                if test_cap.isOpened():
                    ret, frame = test_cap.read()
                    if ret:
                        logger.info(f"✅ Kamera {i} bulundu ve çalışıyor")
                        test_cap.release()
                        SETTINGS.CAMERA_INDEX = i  # Çalışan kamerayı kullan
                        cap = cv2.VideoCapture(i)
                        break
                test_cap.release()
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                height, width = frame.shape[:2]
                logger.info(f"✅ Kamera çalışıyor - Çözünürlük: {width}x{height}")
                cap.release()
                return True
            else:
                logger.error("❌ Kamera açık ama görüntü alınamıyor")
        
        cap.release()
        return False
        
    except Exception as e:
        logger.error(f"❌ Kamera testi sırasında hata: {str(e)}")
        return False

def setup_environment():
    """
    Sistem ortamını hazırla.
    """
    logger = get_logger("startup")
    
    # Gerekli klasörleri oluştur
    logger.info("Gerekli klasörler oluşturuluyor...")
    SETTINGS.create_directories()
    
    # Ayarları doğrula
    logger.info("Sistem ayarları doğrulanıyor...")
    validation_errors = SETTINGS.validate_settings()
    if validation_errors:
        logger.warning("⚠️  Ayar uyarıları:")
        for error in validation_errors:
            logger.warning(f"  - {error}")
    
    # Sistem bilgilerini logla
    log_manager.log_system_info()
    
    logger.info("✅ Sistem ortamı hazırlandı")

def main():
    """Ana fonksiyon"""
    # Logo ve başlangıç mesajı
    print("=" * 60)
    print("🏪 OpenCV Müşteri Analiz Sistemi")
    print("   Gümüş Takı ve Saat Dükkânları için AI Destekli Analiz")
    print("=" * 60)
    print("📋 Sistem Durumu Kontrol Ediliyor...")
    print("   - Python sürümü kontrol ediliyor...")
    print("   - Kütüphaneler kontrol ediliyor...")
    print("   - Kamera erişimi test ediliyor...")
    print()
    
    logger = get_logger("main")
    
    try:
        logger.info("🚀 Sistem başlatılıyor...")
        
        # 1. Sistem ortamını hazırla
        setup_environment()
        
        # 2. Gereksinimleri kontrol et
        if not check_dependencies():
            logger.error("❌ Kritik sistem gereksinimleri karşılanmıyor")
            print("\n🔧 ÇÖZÜM SEÇENEKLERİ:")
            print("1. Otomatik kurulum (önerilen):")
            print("   .\\quick_setup.ps1")
            print("\n2. Minimal kütüphaneleri manuel yükle:")
            print("   pip install -r requirements_minimal.txt")
            print("\n3. Tek tek yükle:")
            print("   pip install opencv-python numpy pillow")
            
            response = input("\nYine de devam etmek istiyor musunuz? (e/h): ").lower().strip()
            if response not in ['e', 'evet', 'y', 'yes']:
                logger.info("Kullanıcı tarafından iptal edildi")
                return 1
            
            logger.warning("⚠️  Kritik kütüphaneler eksik - sistem hatalı çalışabilir")
        
        # 3. Kamera kontrolü
        camera_available = check_camera()
        if not camera_available:
            logger.warning("⚠️  Kamera bulunamadı veya erişilemiyor")
            logger.warning("Sistem kamera olmadan da çalıştırılabilir (test modunda)")
            
            response = input("\nKamera olmadan devam etmek istiyor musunuz? (e/h): ").lower().strip()
            if response not in ['e', 'evet', 'y', 'yes']:
                logger.info("Kullanıcı tarafından iptal edildi")
                return 1
        
        # 4. Ana pencereyi başlat
        logger.info("🖥️  Ana pencere başlatılıyor...")
        app = MainWindow()
        
        logger.info("✅ Sistem başarıyla hazırlandı")
        logger.info("🎯 Kullanıcı arayüzü aktif - 'Başlat' butonuna basarak sistemi başlatın")
        
        # 5. Ana döngüyü çalıştır
        app.run()
        
        logger.info("👋 Sistem kapatılıyor...")
        return 0
        
    except KeyboardInterrupt:
        logger.info("💀 Kullanıcı tarafından durduruldu (Ctrl+C)")
        return 0
        
    except Exception as e:
        logger.error("💥 Beklenmeyen hata:")
        logger.error(traceback.format_exc())
        
        print(f"\n❌ Sistem hatası: {str(e)}")
        print("\n📋 Hata detayları log dosyasında:")
        print(f"   📄 {os.path.join(SETTINGS.LOG_DIR, 'sistem.log')}")
        
        print("\n🔧 Muhtemel çözümler:")
        print("1. Kütüphaneleri yeniden yükleyin:")
        print("   .\\quick_setup.ps1  (otomatik)")
        print("2. Sanal ortamı sıfırlayın:")
        print("   Remove-Item -Recurse -Force .venv  (PowerShell)")
        print("   rmdir /s .venv                      (CMD)")
        print("   python -m venv .venv")
        print("3. Python sürümünü kontrol edin (3.8-3.10 önerilen)")
        print("4. Visual Studio C++ Build Tools gerekebilir (dlib için)")
        
        print("\n💬 Destek için:")
        print("   - Test scripti: python test_requirements.py")
        print("   - Minimal kurulum: pip install -r requirements_minimal.txt")
        
        input("\nDevam etmek için Enter'a basın...")
        return 1

if __name__ == "__main__":
    """Uygulama başlangıç noktası"""
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n💥 Kritik hata: {str(e)}")
        print(traceback.format_exc())
        input("\nDevam etmek için Enter'a basın...")
        sys.exit(1) 