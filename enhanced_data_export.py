#!/usr/bin/env python3
"""
Gelişmiş Veri Export ve Analiz Scripti
Mevcut verileri temizleyip daha anlamlı hale getirir
"""

import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

def clean_and_export_data():
    """Mevcut verileri temizle ve anlamlı hale getir"""
    
    print("🧹 Veri temizleme ve iyileştirme başlatılıyor...")
    
    # Database bağlantısı
    db_path = "data/musteri_analiz.db"
    conn = sqlite3.connect(db_path)
    
    # Mevcut verileri oku
    df = pd.read_sql_query("""
        SELECT * FROM visitors 
        ORDER BY entry_time DESC
    """, conn)
    
    print(f"📊 Toplam kayıt: {len(df)}")
    
    # Veri temizleme
    original_count = len(df)
    
    # 1. Confidence 0.0 olanları filtrele
    df_clean = df[df['confidence_avg'] > 0.0].copy()
    print(f"🔧 Confidence > 0.0 filtresi: {len(df_clean)} kayıt kaldı")
    
    # 2. Placeholder bounding box'ları filtrele
    def is_valid_bbox(bbox_str):
        try:
            bboxes = json.loads(bbox_str)
            return not (len(bboxes) == 1 and bboxes[0] == [0, 0, 100, 100])
        except:
            return False
    
    df_clean = df_clean[df_clean['bounding_box'].apply(is_valid_bbox)].copy()
    print(f"🔧 Geçerli bounding box filtresi: {len(df_clean)} kayıt kaldı")
    
    # 3. Tarih/saat formatını düzelt
    df_clean['entry_time'] = pd.to_datetime(df_clean['entry_time'])
    df_clean['date'] = df_clean['entry_time'].dt.date
    df_clean['time'] = df_clean['entry_time'].dt.time
    df_clean['hour'] = df_clean['entry_time'].dt.hour
    df_clean['day_of_week'] = df_clean['entry_time'].dt.day_name()
    
    # 4. Confidence kategorileri ekle
    def confidence_category(conf):
        if conf >= 0.8:
            return "Yüksek"
        elif conf >= 0.6:
            return "Orta"
        elif conf >= 0.4:
            return "Düşük"
        else:
            return "Çok Düşük"
    
    df_clean['confidence_category'] = df_clean['confidence_avg'].apply(confidence_category)
    
    # 5. Bounding box analizi
    def analyze_bbox(bbox_str):
        try:
            bboxes = json.loads(bbox_str)
            if bboxes:
                bbox = bboxes[0]  # İlk bbox'ı al
                x, y, w, h = bbox
                area = w * h
                center_x = x + w/2
                center_y = y + h/2
                
                # Kamera bölgesi analizi (1280x720 için)
                if center_x < 426:
                    region = "Sol"
                elif center_x < 854:
                    region = "Merkez"
                else:
                    region = "Sağ"
                
                return {
                    'area': area,
                    'center_x': int(center_x),
                    'center_y': int(center_y),
                    'region': region,
                    'width': w,
                    'height': h
                }
        except:
            pass
        return {'area': 0, 'center_x': 0, 'center_y': 0, 'region': 'Bilinmiyor', 'width': 0, 'height': 0}
    
    bbox_analysis = df_clean['bounding_box'].apply(analyze_bbox)
    df_clean['detection_area'] = [ba['area'] for ba in bbox_analysis]
    df_clean['detection_region'] = [ba['region'] for ba in bbox_analysis]
    df_clean['person_width'] = [ba['width'] for ba in bbox_analysis]
    df_clean['person_height'] = [ba['height'] for ba in bbox_analysis]
    
    # 6. Zaman dilimi kategorileri
    def time_period(hour):
        if 6 <= hour < 12:
            return "Sabah"
        elif 12 <= hour < 17:
            return "Öğleden Sonra"
        elif 17 <= hour < 21:
            return "Akşam"
        else:
            return "Gece"
    
    df_clean['time_period'] = df_clean['hour'].apply(time_period)
    
    # 7. Gelişmiş CSV export
    export_columns = [
        'id', 'entry_time', 'date', 'time', 'hour', 'day_of_week', 'time_period',
        'confidence_avg', 'confidence_category', 
        'detection_area', 'detection_region', 'person_width', 'person_height',
        'camera_index', 'detection_count'
    ]
    
    # Export dosyası
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_file = f"data/csv_backups/enhanced_visitor_data_{timestamp}.csv"
    
    df_clean[export_columns].to_csv(export_file, index=False, encoding='utf-8')
    
    # Özet istatistikler
    print("\n📈 VERİ ÖZETİ:")
    print(f"📊 Temizlenen kayıt sayısı: {len(df_clean)} (orijinal: {original_count})")
    print(f"📅 Tarih aralığı: {df_clean['date'].min()} - {df_clean['date'].max()}")
    print(f"⭐ Ortalama confidence: {df_clean['confidence_avg'].mean():.1%}")
    
    print("\n🕐 SAAT DİLİMİ ANALİZİ:")
    time_analysis = df_clean.groupby('time_period').size()
    for period, count in time_analysis.items():
        print(f"  {period}: {count} ziyaretçi")
    
    print("\n📍 BÖLGE ANALİZİ:")
    region_analysis = df_clean.groupby('detection_region').size()
    for region, count in region_analysis.items():
        print(f"  {region}: {count} tespit")
    
    print("\n⭐ CONFİDENCE KATEGORİLERİ:")
    conf_analysis = df_clean.groupby('confidence_category').size()
    for category, count in conf_analysis.items():
        print(f"  {category}: {count} tespit")
    
    print(f"\n✅ Gelişmiş veri dosyası kaydedildi: {export_file}")
    
    # Günlük özet
    today = datetime.now().date()
    today_data = df_clean[df_clean['date'] == today]
    
    if len(today_data) > 0:
        print(f"\n🎯 BUGÜNÜN ÖZETİ ({today}):")
        print(f"  📊 Toplam ziyaretçi: {len(today_data)}")
        print(f"  ⭐ Ortalama confidence: {today_data['confidence_avg'].mean():.1%}")
        print(f"  🕐 En yoğun saat: {today_data['hour'].mode().iloc[0]:02d}:00")
        print(f"  📍 En çok tespit edilen bölge: {today_data['detection_region'].mode().iloc[0]}")
    
    conn.close()
    return export_file

def generate_daily_report():
    """Günlük rapor oluştur"""
    
    print("\n📋 GÜNLÜK RAPOR OLUŞTURULUYOR...")
    
    db_path = "data/musteri_analiz.db"
    conn = sqlite3.connect(db_path)
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    # Bugün ve dün karşılaştırması
    today_query = f"""
        SELECT COUNT(*) as count, AVG(confidence_avg) as avg_conf
        FROM visitors 
        WHERE DATE(entry_time) = '{today}' AND confidence_avg > 0.0
    """
    
    yesterday_query = f"""
        SELECT COUNT(*) as count, AVG(confidence_avg) as avg_conf
        FROM visitors 
        WHERE DATE(entry_time) = '{yesterday}' AND confidence_avg > 0.0
    """
    
    today_stats = pd.read_sql_query(today_query, conn).iloc[0]
    yesterday_stats = pd.read_sql_query(yesterday_query, conn).iloc[0]
    
    # Saatlik dağılım
    hourly_query = f"""
        SELECT strftime('%H', entry_time) as hour, COUNT(*) as count
        FROM visitors 
        WHERE DATE(entry_time) = '{today}' AND confidence_avg > 0.0
        GROUP BY hour
        ORDER BY hour
    """
    
    hourly_data = pd.read_sql_query(hourly_query, conn)
    
    # Rapor dosyası
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"data/csv_backups/daily_report_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"🏪 GÜNLÜK ZİYARETÇİ RAPORU\n")
        f.write(f"📅 Tarih: {today}\n")
        f.write(f"🕐 Rapor Zamanı: {datetime.now().strftime('%H:%M:%S')}\n")
        f.write("="*50 + "\n\n")
        
        f.write("📊 GENEL İSTATİSTİKLER:\n")
        f.write(f"  Bugün Toplam Ziyaretçi: {today_stats['count']}\n")
        f.write(f"  Dün Toplam Ziyaretçi: {yesterday_stats['count']}\n")
        
        if yesterday_stats['count'] > 0:
            change = ((today_stats['count'] - yesterday_stats['count']) / yesterday_stats['count']) * 100
            f.write(f"  Değişim: {change:+.1f}%\n")
        
        f.write(f"  Bugün Ortalama Confidence: {today_stats['avg_conf']:.1%}\n\n")
        
        f.write("🕐 SAATLİK DAĞILIM:\n")
        for _, row in hourly_data.iterrows():
            f.write(f"  {row['hour']}:00 - {row['count']} ziyaretçi\n")
    
    print(f"✅ Günlük rapor kaydedildi: {report_file}")
    
    conn.close()
    return report_file

if __name__ == "__main__":
    try:
        # Veri temizleme ve export
        enhanced_file = clean_and_export_data()
        
        # Günlük rapor
        report_file = generate_daily_report()
        
        print(f"\n🎉 İŞLEM TAMAMLANDI!")
        print(f"📁 Gelişmiş veri: {enhanced_file}")
        print(f"📋 Günlük rapor: {report_file}")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc() 