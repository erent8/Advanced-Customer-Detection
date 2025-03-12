import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Tuple, Optional
import numpy as np
from pathlib import Path
import gc

from src.analytics import CustomerAnalytics
from src.logger import log_error

# Stil ayarları
plt.style.use('default')  # Varsayılan matplotlib stili
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.figsize'] = [12, 6]
plt.rcParams['axes.unicode_minus'] = False

class CustomerVisualization:
    """Müşteri verilerini görselleştirme sınıfı."""
    
    def __init__(self, analytics: CustomerAnalytics):
        """
        Müşteri verilerini görselleştirmek için sınıf.
        
        Args:
            analytics (CustomerAnalytics): Müşteri analiz verileri
        """
        self.analytics = analytics
        self.output_dir = Path(__file__).parent.parent / "reports" / "graphs"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def _save_plot(self, filename: str) -> str:
        """
        Grafiği kaydet ve belleği temizle
        
        Args:
            filename (str): Kaydedilecek dosya adı
        """
        try:
            full_path = self.output_dir / f"{filename}.png"
            plt.savefig(full_path, dpi=300, bbox_inches='tight')
            return str(full_path)
        except Exception as e:
            log_error(f"Grafik kaydedilirken hata oluştu: {e}")
            raise
        finally:
            plt.close('all')
            gc.collect()
    
    def _validate_data(self, data: Optional[Dict]) -> bool:
        """Veri geçerliliğini kontrol et."""
        if data is None:
            return False
        if isinstance(data, dict) and not data:
            return False
        return True
    
    def plot_hourly_distribution(self):
        """Saatlik müşteri dağılımı grafiği"""
        try:
            hourly_data = self.analytics.get_hourly_stats()
            if not hourly_data:
                log_error("Saatlik dağılım verisi boş")
                return False
                
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(hourly_data.keys(), hourly_data.values())
            ax.set_xlabel("Saat")
            ax.set_ylabel("Müşteri Sayısı")
            ax.set_title("Saatlik Müşteri Dağılımı")
            plt.tight_layout()
            self._save_plot("hourly_distribution")
            return True
        except Exception as e:
            log_error(f"Saatlik dağılım grafiği oluşturulurken hata: {str(e)}")
            return False
    
    def plot_daily_trend(self):
        """Günlük müşteri trendi grafiği"""
        try:
            daily_data = self.analytics.get_daily_report()
            if not daily_data:
                log_error("Günlük trend verisi boş")
                return False
                
            dates = list(daily_data.keys())
            values = [data['toplam_musteri'] for data in daily_data.values()]
                
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(dates, values, marker='o')
            ax.set_xlabel("Tarih")
            ax.set_ylabel("Müşteri Sayısı")
            ax.set_title("Günlük Müşteri Trendi")
            ax.grid(True)
            plt.xticks(rotation=45)
            self._save_plot("daily_trend")
            return True
        except Exception as e:
            log_error(f"Günlük trend grafiği oluşturulurken hata: {str(e)}")
            return False
    
    def plot_weekly_comparison(self):
        """Haftalık karşılaştırma grafiği"""
        try:
            weekly_data = self.analytics.get_weekly_report()
            if not weekly_data:
                log_error("Haftalık karşılaştırma verisi boş")
                return False
                
            weeks = list(weekly_data.keys())
            total_customers = [data['toplam_musteri'] for data in weekly_data.values()]
            avg_customers = [data['ortalama_musteri'] for data in weekly_data.values()]
                
            fig, ax = plt.subplots(figsize=(12, 6))
            x = range(len(weeks))
            width = 0.35
                
            ax.bar([i - width/2 for i in x], total_customers, width, label='Toplam Müşteri')
            ax.bar([i + width/2 for i in x], avg_customers, width, label='Ortalama Müşteri')
                
            ax.set_xlabel("Hafta")
            ax.set_ylabel("Müşteri Sayısı")
            ax.set_title("Haftalık Müşteri Karşılaştırması")
            plt.xticks(x, weeks, rotation=45)
            ax.legend()
            plt.tight_layout()
                
            self._save_plot("weekly_comparison")
            return True
        except Exception as e:
            log_error(f"Haftalık karşılaştırma grafiği oluşturulurken hata: {str(e)}")
            return False
    
    def create_heatmap(self, days: int = 30):
        """Saatlik yoğunluk ısı haritası"""
        try:
            current_date = datetime.now()
            data = []
            
            for day in range(days):
                date = current_date - timedelta(days=day)
                stats = self.analytics.get_hourly_stats(date)
                if stats:
                    data.append(list(stats.values()))
            
            if not data:
                log_error("Isı haritası verisi boş")
                return False
            
            plt.figure(figsize=(12, 8))
            sns.heatmap(data, 
                       cmap='YlOrRd',
                       xticklabels=range(24),
                       yticklabels=range(days),
                       cbar_kws={'label': 'Müşteri Sayısı'})
            
            plt.title("Müşteri Yoğunluğu Isı Haritası")
            plt.xlabel("Saat")
            plt.ylabel("Gün")
            plt.tight_layout()
            
            self._save_plot("heatmap")
            return True
        except Exception as e:
            log_error(f"Isı haritası oluşturulurken hata: {str(e)}")
            return False
    
    def plot_visit_duration_distribution(self):
        """Ziyaret süresi dağılımı grafiği"""
        try:
            duration_data = self.analytics.get_visit_duration_stats()
            if not duration_data:
                log_error("Ziyaret süresi verisi boş")
                return False
                
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(['Ortalama', 'Minimum', 'Maksimum', 'Medyan'],
                    [duration_data['ortalama_sure'],
                     duration_data['minimum_sure'],
                     duration_data['maksimum_sure'],
                     duration_data['medyan_sure']])
                
            ax.set_xlabel("Metrik")
            ax.set_ylabel("Süre (saniye)")
            ax.set_title("Ziyaret Süresi Dağılımı")
            plt.xticks(rotation=45)
                
            self._save_plot("visit_duration")
            return True
        except Exception as e:
            log_error(f"Ziyaret süresi grafiği oluşturulurken hata: {str(e)}")
            return False 