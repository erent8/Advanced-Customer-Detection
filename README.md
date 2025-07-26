# 🏪 OpenCV Müşteri Analiz Sistemi

Gümüş takı ve saat dükkânları için geliştirilmiş yapay zekâ destekli müşteri analiz sistemi. Bu sistem, kamera görüntüleri kullanarak müşteri trafiğini analiz eder, demografik bilgiler toplar ve iş kararlarına destek olacak detaylı raporlar sunar.

## 🎯 Özellikler

### Mevcut Özellikler (v1.0)
- ✅ **Gerçek Zamanlı Kamera Görüntüsü**: OpenCV ile canlı video akışı
- ✅ **İnsan Tespiti**: YOLOv8 ile yüksek doğrulukta kişi tanıma
- ✅ **Temel Ziyaretçi Sayımı**: Günlük müşteri trafiği takibi
- ✅ **Veri Kaydetme**: CSV ve SQLite ile güvenli veri depolama

### Gelecek Özellikler
- 🔄 **Çalışan Filtreleme**: Yüz tanıma ile çalışanları sayımdan çıkarma
- 🔄 **Demografik Analiz**: Yaş ve cinsiyet tahmini
- 🔄 **Yoğunluk Analizi**: Saatlik/günlük trafik raporları
- 🔄 **Geri Gelen Müşteri Tespiti**: Tekrar eden ziyaretçi analizi
- 🔄 **Dashboard**: Web tabanlı görselleştirme paneli

## 🚀 Kurulum

### Sistem Gereksinimleri
- **Python**: 3.8 veya üzeri
- **İşletim Sistemi**: Windows 10/11, macOS, Linux
- **Kamera**: USB kamera veya laptop kamerası
- **RAM**: Minimum 4GB (8GB önerilir)
- **Depolama**: 2GB boş alan

### Adım 1: Projeyi İndirin
```bash
git clone <repo-url>
cd OpenCV-Customer-Detection
```

### Adım 2: Sanal Ortam Oluşturun
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux  
source venv/bin/activate
```

### Adım 3: Kütüphaneleri Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 4: İlk Çalıştırma
```bash
python src/main.py
```

## 📁 Proje Yapısı

```
OpenCV-Customer-Detection/
├── src/                    # Ana kaynak kodlar
│   ├── core/              # Ana işlem modülleri
│   ├── models/            # ML modelleri ve ağırlıklar
│   ├── utils/             # Yardımcı fonksiyonlar
│   ├── config/            # Konfigürasyon dosyaları
│   ├── data/              # Veri depolama
│   └── ui/                # Kullanıcı arayüzü
├── data/                  # Veri dosyaları
│   ├── csv_backups/       # CSV yedekleri
│   └── employee_faces/    # Çalışan yüz fotoğrafları
├── logs/                  # Log dosyaları
├── models/                # AI model dosyaları
├── requirements.txt       # Python bağımlılıkları
├── .cursorrules.md       # Geliştirme kuralları
└── README.md             # Bu dosya
```

## ⚙️ Konfigürasyon

Ana ayarlar `src/config/settings.py` dosyasında bulunur:

```python
# Kamera ayarları
CAMERA_INDEX = 0          # Kamera seçimi
CAMERA_WIDTH = 1280       # Görüntü genişliği
CAMERA_HEIGHT = 720       # Görüntü yüksekliği

# Tespit ayarları  
DETECTION_CONFIDENCE = 0.5  # Tespit hassasiyeti
DUPLICATE_PREVENTION_TIME = 30  # Tekrar sayımı engelleme (saniye)
```

## 🔧 Kullanım

### Temel Kullanım
1. Sistemi çalıştırın: `python src/main.py`
2. Kamera görüntüsü otomatik olarak başlar
3. İnsanlar tespit edildiğinde yeşil çerçeve ile işaretlenir
4. Ziyaretçi sayısı gerçek zamanlı güncellenir

### Veri Görüntüleme
- **Günlük veriler**: `data/` klasöründeki CSV dosyaları
- **Veritabanı**: `data/musteri_analiz.db` SQLite dosyası
- **Loglar**: `logs/` klasöründeki log dosyaları

## 📊 Veri Formatı

### Ziyaretçi Verisi (CSV)
```csv
tarih,saat,ziyaretci_id,tespit_zamani,cinsiyet,yas_kategorisi,calisanmi
2024-01-15,14:30:25,VIS_001,2024-01-15 14:30:25,Belirsiz,Belirsiz,False
```

### SQLite Tabloları
- `ziyaretciler`: Temel ziyaretçi bilgileri
- `tespitler`: Her tespit anı kayıtları  
- `calisanlar`: Çalışan yüz verileri (hash'li)

## 🛠️ Geliştirme

### Katkıda Bulunma
1. Bu projeyi fork edin
2. Yeni özellik dalı oluşturun: `git checkout -b yeni-ozellik`
3. Değişikliklerinizi commit edin: `git commit -am 'feat: Yeni özellik eklendi'`
4. Dalınızı push edin: `git push origin yeni-ozellik`
5. Pull Request oluşturun

### Geliştirme Kuralları
- `.cursorrules.md` dosyasındaki kurallara uyun
- Türkçe yorumlar kullanın
- PEP 8 standartlarına uygun kod yazın
- Her fonksiyona docstring ekleyin

### Test Etme
```bash
# Unit testler
python -m pytest tests/

# Kod kalitesi kontrol
flake8 src/
black src/
```

## 🔒 Gizlilik ve Güvenlik

- ✅ **Yerel Depolama**: Tüm veriler yerel olarak saklanır
- ✅ **Veri Şifreleme**: Yüz verileri hash'lenmiş şekilde tutulur  
- ✅ **GDPR Uyumlu**: Kişisel veri koruma kurallarına uygun
- ✅ **Anonim Kayıt**: Kişi kimliği saklanmaz

## 📈 Performans

### Sistem Gereksinimleri
- **CPU**: Intel i5 veya AMD Ryzen 5 (önerilen)
- **GPU**: NVIDIA GTX 1050 veya üzeri (opsiyonel hızlandırma)
- **FPS**: 15-30 FPS (donanıma göre değişir)

### Optimizasyon İpuçları
- GPU kullanımı için: `YOLO_DEVICE = "cuda"` ayarlayın
- Düşük çözünürlük için: `PROCESS_WIDTH/HEIGHT` değerlerini azaltın
- Çoklu işlemci için: `PROCESSING_THREAD_COUNT` artırın

## 🆘 Sorun Giderme

### Sık Karşılaşılan Sorunlar

**Kamera açılmıyor:**
```bash
# Kamera indeksini kontrol edin
CAMERA_INDEX = 1  # settings.py dosyasında
```

**Yavaş performans:**
```bash
# İşlem boyutunu küçültün
PROCESS_WIDTH = 320
PROCESS_HEIGHT = 240
```

**Model yüklenmiyor:**
```bash
# YOLOv8 modelini manuel indirin
pip install ultralytics
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### Loglara Bakın
```bash
# Son logları görüntüle
tail -f logs/sistem.log
```

## 📋 Sürüm Geçmişi

- **v1.0.0** (2024-01-15): İlk sürüm - Temel kamera ve tespit sistemi
- **v0.9.0** (2024-01-10): Alpha sürüm - Prototip geliştirme

## 📞 İletişim

- **Geliştirici**: Müşteri Analiz Sistemi Takımı
- **E-posta**: [iletisim@musteri-analiz.com](mailto:iletisim@musteri-analiz.com)
- **GitHub**: [https://github.com/musteri-analiz/opencv-customer-detection](https://github.com/musteri-analiz/opencv-customer-detection)

## 📄 Lisans

Bu proje MIT lisansı altında yayınlanmıştır. Detaylar için `LICENSE` dosyasını inceleyin.

---

**⭐ Bu projeyi faydalı bulduysanız yıldızlamayı unutmayın!** 