# Göz Kırpma Algılayıcı - Uykusuzluk Tespit Sistemi

## Proje Hakkında
Bu proje, sürücülerin uykulu olup olmadığını gerçek zamanlı olarak tespit eden bir bilgisayar görüşü uygulamasıdır. Sistem, sürücünün gözlerini sürekli olarak izler ve göz kapalı kalma süresini analiz ederek uykulu sürüş durumunu tespit eder.

## Özellikler
- 🎥 Gerçek zamanlı video analizi
- 👁️ Göz kırpma tespiti
- ⏱️ Göz kapalı kalma süresi ölçümü
- 🚨 Sesli uyarı sistemi
- 📊 Göz açıklık oranı (EAR) görselleştirmesi

## Teknik Detaylar
Sistem şu teknolojileri kullanmaktadır:
- **Python**: Ana programlama dili
- **OpenCV**: Görüntü işleme ve video yakalama
- **dlib**: Yüz ve yüz noktalarının tespiti
- **scipy**: Öklid mesafesi hesaplamaları
- **pygame**: Sesli uyarı sistemi

### Göz Açıklık Oranı (EAR) Hesaplaması
EAR (Eye Aspect Ratio) şu formül kullanılarak hesaplanır:
```
EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
```
Burada:
- p1-p6: Göz çevresindeki 6 referans noktası
- ||.||: İki nokta arasındaki Öklid mesafesi

## Kurulum

### Sistem Gereksinimleri
- Python 3.7 veya üzeri
- Webcam
- Windows/Linux/MacOS işletim sistemi

### Adım Adım Kurulum
1. **Python Kurulumu**
   ```bash
   # Python'u indirin ve kurun (python.org)
   # PATH'e eklemeyi unutmayın
   ```

2. **Sanal Ortam Oluşturma**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows için
   source .venv/bin/activate # Linux/MacOS için
   ```

3. **Gerekli Paketlerin Kurulumu**
   ```bash
   pip install -r requirements.txt
   ```

4. **Yüz Landmark Dosyasının İndirilmesi**
   - shape_predictor_68_face_landmarks.dat dosyasını indirin
   - Proje klasörüne kopyalayın

## Kullanım Kılavuzu

### Programı Başlatma
```bash
python drowsiness_detection.py
```

### Kontroller
- **q**: Programdan çıkış
- Program çalışırken webcam görüntüsü ekranda görünecektir
- Göz açıklık oranı (EAR) ekranın üst kısmında gösterilir
- Uykulu sürüş tespit edildiğinde sesli ve görsel uyarı verilir

### Parametrelerin Ayarlanması
Programdaki önemli parametreler:
- `EAR_THRESHOLD`: Göz kapalı kabul edilecek EAR değeri (varsayılan: 0.25)
- `CONSECUTIVE_FRAMES`: Uyarı vermek için gereken ardışık kare sayısı (varsayılan: 20)

Bu değerler `drowsiness_detection.py` dosyasından ayarlanabilir.

## Test Etme
Sistemin doğru çalıştığını kontrol etmek için test senaryoları eklenmiştir:
```bash
python -m unittest test_drowsiness_detection.py -v
```

Testler şunları kontrol eder:
- EAR hesaplamasının doğruluğu
- Göz noktalarının doğru tespiti
- Açık/kapalı göz durumlarının ayrımı
- Hata durumlarının yönetimi

## Güvenlik Uyarıları
- Bu sistem sürüş güvenliğini destekleyici bir araçtır, tek başına güvenilmemelidir
- Sistem performansı ışık koşullarından etkilenebilir
- Gözlük kullanımı tespit doğruluğunu etkileyebilir

## Sorun Giderme
1. **Kamera Erişim Hatası**
   - Kamera bağlantısını kontrol edin
   - Başka bir uygulamanın kamerayı kullanmadığından emin olun

2. **dlib Kurulum Hatası**
   - Visual Studio Build Tools'un kurulu olduğundan emin olun
   - CMake'in doğru kurulduğunu kontrol edin

3. **Düşük Performans**
   - Bilgisayarınızın sistem gereksinimlerini karşıladığından emin olun
   - Arka planda çalışan gereksiz uygulamaları kapatın

## Katkıda Bulunma
1. Bu depoyu fork edin
2. Yeni bir branch oluşturun
3. Değişikliklerinizi commit edin
4. Branch'inizi push edin
5. Pull request oluşturun

## İletişim
Sorularınız ve önerileriniz için bir Issue açabilirsiniz.

## Lisans
Bu proje açık kaynak kodlu olarak geliştirilmiştir.