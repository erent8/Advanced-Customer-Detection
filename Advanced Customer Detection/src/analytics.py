from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from sqlalchemy import func, and_, text, extract
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from collections import defaultdict

from src.models import CustomerDetection
from src.logger import log_error

class CustomerAnalytics:
    """Müşteri analitik sınıfı."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_current_customer_count(self) -> int:
        """Mevcut müşteri sayısını döndür."""
        try:
            # Son 5 dakika içindeki en son tespiti al
            last_detection = (
                self.db.query(CustomerDetection)
                .order_by(CustomerDetection.timestamp.desc())
                .first()
            )
            
            if last_detection:
                return last_detection.customer_count
            return 0
            
        except Exception as e:
            log_error(f"Mevcut müşteri sayısı alınırken hata: {str(e)}")
            return 0
    
    def get_hourly_stats(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, List[float]]:
        """Saatlik müşteri yoğunluğunu hesapla."""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=7)
        if end_date is None:
            end_date = datetime.now()
            
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        try:
            # Saatlik ve günlük müşteri sayılarını al
            stats = (
                self.db.query(
                    func.strftime('%w', CustomerDetection.timestamp).label('day'),
                    func.strftime('%H', CustomerDetection.timestamp).label('hour'),
                    func.avg(CustomerDetection.customer_count).label('avg_count')
                )
                .filter(
                    and_(
                        CustomerDetection.timestamp >= start_date,
                        CustomerDetection.timestamp <= end_date
                    )
                )
                .group_by('day', 'hour')
                .all()
            )
            
            # Sonuçları matrise dönüştür
            heatmap_data = np.zeros((24, 7))  # 24 saat x 7 gün
            for day, hour, count in stats:
                if day is not None and hour is not None:
                    heatmap_data[int(hour), int(day)] = float(count)
            
            return heatmap_data.tolist()
            
        except Exception as e:
            log_error(f"Saatlik istatistikler hesaplanırken hata: {str(e)}")
            return np.zeros((24, 7)).tolist()
    
    def get_daily_report(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, Dict]:
        """Günlük müşteri raporunu oluştur."""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=7)
        if end_date is None:
            end_date = datetime.now()
            
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        try:
            # Günlük toplam ve ortalama müşteri sayısını al
            daily_stats = (
                self.db.query(
                    func.strftime('%Y-%m-%d', CustomerDetection.timestamp).label('date'),
                    func.sum(CustomerDetection.customer_count).label('total_count'),
                    func.avg(CustomerDetection.customer_count).label('avg_count'),
                    func.count(CustomerDetection.id).label('detection_count')
                )
                .filter(
                    and_(
                        CustomerDetection.timestamp >= start_date,
                        CustomerDetection.timestamp <= end_date
                    )
                )
                .group_by('date')
                .all()
            )
            
            # Tüm günleri doldur (boş günler için 0 değeri)
            result = {}
            current = start_date
            while current <= end_date:
                result[current.strftime('%Y-%m-%d')] = {
                    'toplam_musteri': 0,
                    'ortalama_musteri': 0,
                    'tespit_sayisi': 0
                }
                current += timedelta(days=1)
            
            # Verileri ekle
            for date_str, total, avg, count in daily_stats:
                if date_str:
                    result[date_str] = {
                        'toplam_musteri': int(total),
                        'ortalama_musteri': float(avg),
                        'tespit_sayisi': int(count)
                    }
            
            return result
            
        except Exception as e:
            log_error(f"Günlük rapor oluşturulurken hata: {str(e)}")
            return {}
    
    def get_summary_stats(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, any]:
        """Özet istatistikleri hesapla."""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=7)
        if end_date is None:
            end_date = datetime.now()
            
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        try:
            # Toplam ve ortalama müşteri sayısı
            stats = (
                self.db.query(
                    func.sum(CustomerDetection.customer_count).label('total'),
                    func.avg(CustomerDetection.customer_count).label('average'),
                    func.count(CustomerDetection.id).label('count')
                )
                .filter(
                    and_(
                        CustomerDetection.timestamp >= start_date,
                        CustomerDetection.timestamp <= end_date
                    )
                )
                .first()
            )
            
            # En yoğun gün
            busiest_day = (
                self.db.query(
                    func.strftime('%Y-%m-%d', CustomerDetection.timestamp).label('date'),
                    func.sum(CustomerDetection.customer_count).label('total')
                )
                .filter(
                    and_(
                        CustomerDetection.timestamp >= start_date,
                        CustomerDetection.timestamp <= end_date
                    )
                )
                .group_by('date')
                .order_by(text('total DESC'))
                .first()
            )
            
            if not stats or not busiest_day:
                return {}
            
            return {
                'toplam_musteri': int(stats.total) if stats.total else 0,
                'ortalama_musteri': round(float(stats.average) if stats.average else 0, 1),
                'en_yogun_gun': busiest_day.date if busiest_day.date else '',
                'en_yogun_gun_musteri': int(busiest_day.total) if busiest_day.total else 0
            }
            
        except Exception as e:
            log_error(f"Özet istatistikler hesaplanırken hata: {str(e)}")
            return {}
    
    def get_weekly_report(self) -> Dict[str, Dict[str, float]]:
        """Haftalık müşteri raporunu oluştur."""
        start_date = datetime.now() - timedelta(weeks=4)
        
        try:
            # Haftalık istatistikleri al
            weekly_stats = (
                self.db.query(
                    func.strftime('%Y-%W', CustomerDetection.timestamp).label('week'),
                    func.sum(CustomerDetection.customer_count).label('total_count'),
                    func.avg(CustomerDetection.customer_count).label('avg_count'),
                    func.count(CustomerDetection.id).label('detection_count')
                )
                .filter(CustomerDetection.timestamp >= start_date)
                .group_by('week')
                .all()
            )
            
            return {
                f"Hafta_{week}": {
                    'toplam_musteri': int(total),
                    'ortalama_musteri': float(avg),
                    'tespit_sayisi': int(count)
                }
                for week, total, avg, count in weekly_stats
            }
            
        except Exception as e:
            log_error(f"Haftalık rapor oluşturulurken hata: {str(e)}")
            return {}
    
    def get_monthly_report(self) -> Dict[str, Dict[str, float]]:
        """Aylık müşteri raporunu oluştur."""
        start_date = datetime.now() - timedelta(days=365)
        
        try:
            # Aylık istatistikleri al
            monthly_stats = (
                self.db.query(
                    func.strftime('%Y-%m', CustomerDetection.timestamp).label('month'),
                    func.sum(CustomerDetection.customer_count).label('total_count'),
                    func.avg(CustomerDetection.customer_count).label('avg_count'),
                    func.count(CustomerDetection.id).label('detection_count')
                )
                .filter(CustomerDetection.timestamp >= start_date)
                .group_by('month')
                .all()
            )
            
            return {
                str(month): {
                    'toplam_musteri': int(total),
                    'ortalama_musteri': float(avg),
                    'tespit_sayisi': int(count)
                }
                for month, total, avg, count in monthly_stats
            }
            
        except Exception as e:
            log_error(f"Aylık rapor oluşturulurken hata: {str(e)}")
            return {}
    
    def get_peak_hours(self, days: int = 30) -> List[Tuple[int, float]]:
        """En yoğun saatleri tespit et."""
        start_date = datetime.now() - timedelta(days=days)
        
        try:
            # Saatlik ortalama müşteri sayısını al ve sırala
            peak_hours = (
                self.db.query(
                    func.strftime('%H', CustomerDetection.timestamp).label('hour'),
                    func.avg(CustomerDetection.customer_count).label('avg_count')
                )
                .filter(CustomerDetection.timestamp >= start_date)
                .group_by('hour')
                .order_by(func.avg(CustomerDetection.customer_count).desc())
                .all()
            )
            
            return [(int(hour), float(avg)) for hour, avg in peak_hours]
            
        except Exception as e:
            log_error(f"En yoğun saatler hesaplanırken hata: {str(e)}")
            return []
    
    def get_visit_duration_stats(self) -> Dict[str, float]:
        """Ziyaret süresi istatistiklerini hesapla."""
        try:
            # Son tespitleri al
            detections = (
                self.db.query(CustomerDetection)
                .order_by(CustomerDetection.timestamp.desc())
                .limit(1000)
                .all()
            )
            
            if not detections:
                return {}
            
            # Ziyaret sürelerini hesapla
            visit_durations = []
            current_visit = []
            
            for det in detections:
                if not current_visit:
                    current_visit.append(det)
                    continue
                
                time_diff = (det.timestamp - current_visit[-1].timestamp).total_seconds()
                
                if time_diff <= 300:  # 5 dakika içindeyse aynı ziyaret
                    current_visit.append(det)
                else:
                    if len(current_visit) > 1:
                        duration = (current_visit[0].timestamp - current_visit[-1].timestamp).total_seconds()
                        visit_durations.append(abs(duration))
                    current_visit = [det]
            
            if not visit_durations:
                return {}
            
            # İstatistikleri hesapla
            durations = np.array(visit_durations)
            return {
                'ortalama_sure': float(np.mean(durations)),
                'minimum_sure': float(np.min(durations)),
                'maksimum_sure': float(np.max(durations)),
                'medyan_sure': float(np.median(durations))
            }
            
        except Exception as e:
            log_error(f"Ziyaret süresi istatistikleri hesaplanırken hata: {str(e)}")
            return {} 