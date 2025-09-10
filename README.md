# 🏪 OpenCV Müşteri Tespit Sistemi

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)](https://opencv.org)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange.svg)](https://ultralytics.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/erent8/OpenCV-Customer-Detection?style=social)](https://github.com/erent8/OpenCV-Customer-Detection)

> **Mağazalar için geliştirilmiş yapay zekâ destekli müşteri analiz sistemi**

Real-time kamera görüntüleri kullanarak müşteri trafiğini analiz eden, demografik bilgiler toplayan ve iş kararlarına destek olacak detaylı raporlar sunan akıllı sistem.


## ✨ Özellikler

### 🎯 Mevcut Özellikler
- **🎥 Real-time Kamera**: 1280x720@30fps canlı görüntü akışı
- **🤖 İnsan Tespiti**: YOLOv8 ile %95+ doğrulukta kişi tanıma
- **⚡ Thread-Safe UI**: Donma olmayan, kararlı arayüz
- **📊 Ziyaretçi Sayımı**: Gerçek zamanlı müşteri trafiği takibi
- **💾 Veri Depolama**: SQLite + CSV backup sistemi
- **📸 Screenshot**: Anlık görüntü kaydetme
- **🔧 FPS Monitoring**: Performans takip sistemi
- **🌙 Modern UI**: Dark mode uyumlu Türkçe arayüz

### 🚀 Geliştirme Aşamasında
- **👤 Çalışan Filtreleme**: Yüz tanıma ile çalışan/müşteri ayrımı
- **🧠 Demografik Analiz**: Yaş ve cinsiyet tahmini
- **📈 Analytics Dashboard**: Web tabanlı görselleştirme paneli
- **🔄 Geri Gelen Müşteri**: Tekrar eden ziyaretçi tespiti
- **📱 Mobile Dashboard**: Mobil uyumlu kontrol paneli

## 🚀 Hızlı Başlangıç

### Otomatik Kurulum (Windows)
```powershell
# PowerShell'i yönetici olarak çalıştırın
.\quick_setup.ps1
```

### Manuel Kurulum
```bash
# 1. Projeyi klonlayın
git clone https://github.com/erent8/OpenCV-Customer-Detection.git
cd OpenCV-Customer-Detection

# 2. Sanal ortam oluşturun
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Bağımlılıkları yükleyin
pip install -r requirements_minimal.txt

# 4. Sistemi başlatın
python main.py
```

## 📸 Ekran Görüntüleri
Ekran görselleri yakın zamanda yüklenecektir.
### Ana Arayüz
- **Real-time Detection**: Canlı kamera görüntüsü üzerinde insan tespiti
- **Status Panel**: FPS, tespit sayısı ve sistem durumu
- **Control Buttons**: Başlat/Durdur, Screenshot, Ayarlar

### Analytics Dashboard
- **Günlük Trafik**: Saatlik ziyaretçi dağılımı
- **Demografik İstatistikler**: Yaş ve cinsiyet analizi
- **Trend Analizi**: Haftalık/aylık karşılaştırmalar

## 🛠️ Sistem Mimarisi

```
├── 📁 src/
│   ├── 🎯 core/              # Ana işlem modülleri
│   │   ├── camera.py         # Kamera yönetimi
│   │   ├── detector.py       # YOLOv8 tespit sistemi
│   │   ├── visitor_tracker.py # Ziyaretçi takip
│   │   └── performance_manager.py # Performans optimizasyonu
│   ├── 💾 models/            # Veritabanı yönetimi
│   ├── 🎨 ui/               # Kullanıcı arayüzü
│   ├── ⚙️ config/           # Sistem ayarları
│   └── 🔧 utils/            # Yardımcı fonksiyonlar
├── 📊 data/                 # Veri depolama
├── 📝 logs/                 # Sistem logları
├── 🤖 models/               # AI model dosyaları
└── 🌐 templates/            # Web dashboard
```

## ⚙️ Konfigürasyon

Sistem ayarları `src/config/settings.py` dosyasında özelleştirilebilir:

```python
# 🎥 Kamera Ayarları
CAMERA_INDEX = 0              # Kamera seçimi (0, 1, 2...)
CAMERA_WIDTH = 1280           # Görüntü genişliği
CAMERA_HEIGHT = 720           # Görüntü yüksekliği
FPS_TARGET = 30               # Hedef FPS

# 🎯 Tespit Ayarları
DETECTION_CONFIDENCE = 0.5    # Tespit hassasiyeti (0-1)
NMS_THRESHOLD = 0.4           # Non-max suppression
PROCESS_EVERY_N_FRAMES = 1    # Her N frame'i işle

# 🔄 Performans Ayarları
USE_GPU = True                # GPU kullanımı (varsa)
PROCESS_WIDTH = 640           # İşlem boyutu (performans için)
PROCESS_HEIGHT = 480
```

## 📊 Performans

### Sistem Gereksinimleri
| Bileşen | Minimum | Önerilen |
|---------|---------|----------|
| **CPU** | Intel i3 / AMD Ryzen 3 | Intel i5 / AMD Ryzen 5 |
| **RAM** | 4GB | 8GB+ |
| **GPU** | - | NVIDIA GTX 1050+ |
| **Python** | 3.8+ | 3.9-3.10 |
| **Kamera** | USB 2.0 | USB 3.0+ |

### Performans Metrikleri
- **FPS**: 15-30 (donanıma göre)
- **Tespit Doğruluğu**: %95+
- **Bellek Kullanımı**: ~200-500MB
- **CPU Kullanımı**: %10-30

## 🔧 Geliştirme

### Kod Standartları
- **PEP 8** uyumlu Python kodu
- Türkçe yorumlar ve dokümantasyon
- Thread-safe UI güncellemeleri
- Comprehensive error handling

### Test Etme
```bash
# Sistem gereksinimleri testi
python test_requirements.py

# Kamera ve tespit testi
python test_detection.py

# Web dashboard testi
python test_web_app.py
```

### Katkıda Bulunma
1. Bu projeyi fork edin
2. Feature branch oluşturun: `git checkout -b yeni-ozellik`
3. Değişikliklerinizi commit edin: `git commit -am 'feat: Yeni özellik'`
4. Branch'i push edin: `git push origin yeni-ozellik`
5. Pull Request oluşturun

## 🐛 Sorun Giderme

### Sık Karşılaşılan Problemler

<details>
<summary><strong>🎥 Kamera Erişim Sorunu</strong></summary>

```python
# Farklı kamera indekslerini deneyin
CAMERA_INDEX = 0  # Laptop kamerası
CAMERA_INDEX = 1  # USB kamera
CAMERA_INDEX = 2  # İkinci USB kamera
```
</details>

<details>
<summary><strong>⚡ Performans Sorunları</strong></summary>

```python
# Düşük performanslı sistemler için
PROCESS_WIDTH = 320
PROCESS_HEIGHT = 240
PROCESS_EVERY_N_FRAMES = 3
```
</details>

<details>
<summary><strong>🤖 Model Yükleme Hatası</strong></summary>

```bash
# YOLOv8 modelini manuel indirin
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```
</details>

### Log Analizi
```bash
# Güncel logları görüntüle
Get-Content logs\system.log -Tail 50  # Windows
tail -f logs/system.log               # Linux/macOS
```

## 📈 Roadmap

- [ ] **v1.1**: Web Dashboard ve API
- [ ] **v1.2**: Demografik Analiz (Yaş/Cinsiyet)
- [ ] **v1.3**: Çalışan Yüz Tanıma Sistemi
- [ ] **v1.4**: Mobile App ve Cloud Sync
- [ ] **v2.0**: Multi-Camera Support

## 🤝 Topluluk

- **GitHub Issues**: [Sorun bildirin](https://github.com/erent8/OpenCV-Customer-Detection/issues)
- **Discussions**: [Tartışmalara katılın](https://github.com/erent8/OpenCV-Customer-Detection/discussions)
- **Wiki**: [Dokümantasyon](https://opencv.org/get-started/?utm_source=opcv&utm_medium=home)

## 📞 İletişim

<div align="center">

**Eren Terzi (@erenterzi@protonmail.com)**

[![GitHub](https://img.shields.io/badge/GitHub-erent8-black?style=for-the-badge&logo=github)](https://github.com/erent8)
[![X](https://img.shields.io/badge/X-@therenn8-1DA1F2?style=for-the-badge&logo=x)](https://x.com/therenn8)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-eren--terzi-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/eren-terzi-573224225)
[![Instagram](https://img.shields.io/badge/Instagram-erennt8-E4405F?style=for-the-badge&logo=instagram)](https://instagram.com/erennt8)

📍 **Artvin, Turkey**

</div>

## 📄 Lisans

Bu proje açık kaynak kodlu olarak öğrenme amaçlı olarak geliştirilmiştir.

---

<div align="center">

**⭐ Projeyi faydalı bulduysanız yıldızlamayı unutmayın!**

**🔄 Fork • ⭐ Star • 🐛 Issue • 🔧 PR**



</div> 
