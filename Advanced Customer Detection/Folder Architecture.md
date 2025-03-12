Advanced_Customer_Detection/
│
├── database/                 # Veritabanı işlemleri
│   └── customer_data.db     
│
├── logs/                    # Log kayıtları
│   └── app.log
│
├── reports/                 # Raporlama sistemi
│   └── graphs/             
│       ├── daily.png
│       ├── weekly.png
│       └── monthly.png
│
├── src/                     # Kaynak kodları
│   ├── __init__.py
│   ├── camera.py           # Ana kamera modülü
│   ├── detector.py         # Tespit algoritmaları
│   ├── database.py         # Veritabanı işlemleri
│   └── utils.py            # Yardımcı fonksiyonlar
│
├── tests/                   # Test dosyaları
│   ├── __init__.py
│   ├── test_camera.py
│   └── test_detector.py
│
├── requirements.txt         # Bağımlılıklar
└── README.md               # Proje dokümantasyonu