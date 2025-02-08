from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from sqlalchemy import func, and_
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
    
    def get_hourly_stats(self, date: datetime = None) -> Dict[int, float]:
        """Saatlik müşteri yoğunluğunu hesapla."""
        if date is None:
            date = datetime.now()
        
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        try:
            # Saatlik ortalama müşteri sayısını al
            hourly_stats = (
                self.db.query(
                    func.strftime('%H', CustomerDetection.timestamp).label('hour'),
                    func.avg(CustomerDetection.customer_count).label('avg_count')
                )
                .filter(
                    and_(
                        CustomerDetection.timestamp >= start_date,
                        CustomerDetection.timestamp < end_date
                    )
                )
                .group_by('hour')
                .all()
            )
            
            # Sonuçları sözlüğe dönüştür
            return {
                int(hour): float(avg_count)
                for hour, avg_count in hourly_stats
            }
            
        except Exception as e:
            log_error(e)
            return {}
    
    def get_daily_report(self, start_date: datetime = None) -> Dict[str, float]:
        """Günlük müşteri raporunu oluştur."""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=7)
            
        end_date = datetime.now()
        
        try:
            # Günlük toplam ve ortalama müşteri sayısını al
            daily_stats = (
                self.db.query(
                    func.date(CustomerDetection.timestamp).label('date'),
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
            
            return {
                str(date): {
                    'toplam_musteri': int(total),
                    'ortalama_musteri': float(avg),
                    'tespit_sayisi': int(count)
                }
                for date, total, avg, count in daily_stats
            }
            
        except Exception as e:
            log_error(e)
            return {}
    
    def get_weekly_report(self) -> Dict[str, Dict[str, float]]:
        """Haftalık müşteri raporunu oluştur."""
        start_date = datetime.now() - timedelta(weeks=4)
        
        try:
            # Haftalık istatistikleri al
            weekly_stats = (
                self.db.query(
                    func.strftime('%W', CustomerDetection.timestamp).label('week'),
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
            log_error(e)
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
            log_error(e)
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
            log_error(e)
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
            log_error(e)
            return {} 