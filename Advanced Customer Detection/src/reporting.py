from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Optional
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import xlsxwriter
import json

from src.analytics import CustomerAnalytics
from src.logger import log_error

class CustomerReporting:
    """Müşteri verilerini raporlama sınıfı."""
    
    def __init__(self, analytics: CustomerAnalytics):
        """
        Args:
            analytics (CustomerAnalytics): Müşteri analiz verileri
        """
        self.analytics = analytics
        self.output_dir = Path(__file__).parent.parent / "reports"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_pdf_report(self, start_date: datetime, end_date: datetime, output_file: str = None) -> str:
        """PDF raporu oluştur."""
        try:
            if output_file is None:
                output_file = f"musteri_raporu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                
            pdf = FPDF()
            
            # Başlık sayfası
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(190, 10, 'Müşteri Analiz Raporu', 0, 1, 'C')
            pdf.set_font('Arial', '', 12)
            pdf.cell(190, 10, f'Rapor Dönemi: {start_date.strftime("%Y-%m-%d")} - {end_date.strftime("%Y-%m-%d")}', 0, 1, 'C')
            
            # Özet istatistikler
            pdf.add_page()
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(190, 10, 'Özet İstatistikler', 0, 1, 'L')
            
            daily_data = self.analytics.get_daily_report(start_date)
            duration_data = self.analytics.get_visit_duration_stats()
            
            pdf.set_font('Arial', '', 12)
            stats = [
                f"Toplam Müşteri: {sum(d['toplam_musteri'] for d in daily_data.values())}",
                f"Ortalama Günlük Müşteri: {sum(d['ortalama_musteri'] for d in daily_data.values()) / len(daily_data):.2f}",
                f"Ortalama Ziyaret Süresi: {duration_data['ortalama_sure']:.2f} saniye",
                f"En Uzun Ziyaret: {duration_data['maksimum_sure']:.2f} saniye"
            ]
            
            for stat in stats:
                pdf.cell(190, 10, stat, 0, 1, 'L')
            
            # Grafikler
            self._add_graphs_to_pdf(pdf, start_date, end_date)
            
            # Detaylı veriler
            self._add_detailed_data_to_pdf(pdf, start_date, end_date)
            
            # Raporu kaydet
            output_path = self.output_dir / output_file
            pdf.output(str(output_path))
            
            return str(output_path)
            
        except Exception as e:
            log_error(f"PDF raporu oluşturulurken hata: {str(e)}")
            raise
    
    def _add_graphs_to_pdf(self, pdf: FPDF, start_date: datetime, end_date: datetime):
        """PDF'e grafikleri ekle."""
        try:
            # Müşteri trendi grafiği
            plt.figure(figsize=(10, 6))
            daily_data = self.analytics.get_daily_report(start_date)
            dates = list(daily_data.keys())
            values = [d['toplam_musteri'] for d in daily_data.values()]
            plt.plot(dates, values, marker='o')
            plt.title("Günlük Müşteri Trendi")
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            trend_path = self.output_dir / "temp_trend.png"
            plt.savefig(trend_path)
            plt.close()
            
            pdf.add_page()
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(190, 10, 'Müşteri Trendi', 0, 1, 'L')
            pdf.image(str(trend_path), x=10, y=30, w=190)
            trend_path.unlink()
            
            # Yoğunluk haritası
            plt.figure(figsize=(10, 6))
            days = (end_date - start_date).days + 1
            data = []
            dates = []
            
            for day in range(days):
                date = start_date + timedelta(days=day)
                stats = self.analytics.get_hourly_stats(date)
                if stats:
                    data.append(list(stats.values()))
                    dates.append(date.strftime('%Y-%m-%d'))
            
            sns.heatmap(data, cmap='YlOrRd', xticklabels=range(24), yticklabels=dates)
            plt.title("Müşteri Yoğunluğu Isı Haritası")
            plt.tight_layout()
            
            heatmap_path = self.output_dir / "temp_heatmap.png"
            plt.savefig(heatmap_path)
            plt.close()
            
            pdf.add_page()
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(190, 10, 'Yoğunluk Haritası', 0, 1, 'L')
            pdf.image(str(heatmap_path), x=10, y=30, w=190)
            heatmap_path.unlink()
            
        except Exception as e:
            log_error(f"Grafikler PDF'e eklenirken hata: {str(e)}")
            raise
    
    def _add_detailed_data_to_pdf(self, pdf: FPDF, start_date: datetime, end_date: datetime):
        """PDF'e detaylı verileri ekle."""
        try:
            pdf.add_page()
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(190, 10, 'Detaylı Veriler', 0, 1, 'L')
            
            daily_data = self.analytics.get_daily_report(start_date)
            pdf.set_font('Arial', '', 10)
            
            # Tablo başlıkları
            headers = ['Tarih', 'Toplam Müşteri', 'Ortalama Müşteri', 'Tespit Sayısı']
            col_width = 190 / len(headers)
            
            for header in headers:
                pdf.cell(col_width, 10, header, 1)
            pdf.ln()
            
            # Tablo verileri
            for date, data in daily_data.items():
                pdf.cell(col_width, 10, date, 1)
                pdf.cell(col_width, 10, str(data['toplam_musteri']), 1)
                pdf.cell(col_width, 10, f"{data['ortalama_musteri']:.2f}", 1)
                pdf.cell(col_width, 10, str(data['tespit_sayisi']), 1)
                pdf.ln()
                
        except Exception as e:
            log_error(f"Detaylı veriler PDF'e eklenirken hata: {str(e)}")
            raise
    
    def export_to_excel(self, start_date: datetime, end_date: datetime, output_file: str = None) -> str:
        """Verileri Excel dosyasına aktar."""
        try:
            if output_file is None:
                output_file = f"musteri_verileri_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                
            output_path = self.output_dir / output_file
            
            with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                # Günlük veriler
                daily_data = self.analytics.get_daily_report(start_date)
                df_daily = pd.DataFrame.from_dict(daily_data, orient='index')
                df_daily.to_excel(writer, sheet_name='Günlük Veriler')
                
                # Saatlik veriler
                hourly_data = {}
                current_date = start_date
                while current_date <= end_date:
                    stats = self.analytics.get_hourly_stats(current_date)
                    if stats:
                        hourly_data[current_date.strftime('%Y-%m-%d')] = stats
                    current_date += timedelta(days=1)
                
                df_hourly = pd.DataFrame.from_dict(hourly_data, orient='index')
                df_hourly.to_excel(writer, sheet_name='Saatlik Veriler')
                
                # Ziyaret süreleri
                duration_data = self.analytics.get_visit_duration_stats()
                df_duration = pd.DataFrame([duration_data])
                df_duration.to_excel(writer, sheet_name='Ziyaret Süreleri')
                
                # Formatlamalar
                workbook = writer.book
                
                # Sayı formatı
                number_format = workbook.add_format({'num_format': '#,##0.00'})
                
                for sheet in writer.sheets.values():
                    sheet.set_column('A:Z', 15, number_format)
            
            return str(output_path)
            
        except Exception as e:
            log_error(f"Excel export işlemi sırasında hata: {str(e)}")
            raise
    
    def export_to_json(self, start_date: datetime, end_date: datetime, output_file: str = None) -> str:
        """Verileri JSON dosyasına aktar."""
        try:
            if output_file is None:
                output_file = f"musteri_verileri_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                
            output_path = self.output_dir / output_file
            
            export_data = {
                'meta': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'generated_at': datetime.now().isoformat()
                },
                'daily_data': self.analytics.get_daily_report(start_date),
                'hourly_data': {},
                'visit_duration': self.analytics.get_visit_duration_stats()
            }
            
            # Saatlik verileri topla
            current_date = start_date
            while current_date <= end_date:
                stats = self.analytics.get_hourly_stats(current_date)
                if stats:
                    export_data['hourly_data'][current_date.strftime('%Y-%m-%d')] = stats
                current_date += timedelta(days=1)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            return str(output_path)
            
        except Exception as e:
            log_error(f"JSON export işlemi sırasında hata: {str(e)}")
            raise 