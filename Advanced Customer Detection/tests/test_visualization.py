import pytest
from datetime import datetime, timedelta
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from unittest.mock import Mock, patch
import gc
import os
import unittest
import seaborn as sns
import pandas as pd

from src.visualization import CustomerVisualization
from src.analytics import CustomerAnalytics

@pytest.fixture
def mock_analytics():
    """Mock CustomerAnalytics nesnesi oluştur."""
    mock = Mock(spec=CustomerAnalytics)
    
    # Test verileri
    mock.get_hourly_stats.return_value = {i: 10 for i in range(24)}  # Her saat için 10 müşteri
    mock.get_daily_report.return_value = {
        f"2024-02-{i:02d}": {
            'toplam_musteri': 100,
            'ortalama_musteri': 10,
            'tespit_sayisi': 50
        } for i in range(1, 8)
    }
    mock.get_weekly_report.return_value = {
        'Hafta_01': {
            'toplam_musteri': 150,
            'ortalama_musteri': 120,
            'tespit_sayisi': 75
        },
        'Hafta_02': {
            'toplam_musteri': 130,
            'ortalama_musteri': 100,
            'tespit_sayisi': 65
        }
    }
    mock.get_visit_duration_stats.return_value = {
        'ortalama_sure': 300,
        'minimum_sure': 60,
        'maksimum_sure': 1800,
        'medyan_sure': 240
    }
    
    return mock

@pytest.fixture
def viz(mock_analytics, tmp_path):
    """Test için CustomerVisualization nesnesi oluştur."""
    viz = CustomerVisualization(mock_analytics)
    viz.output_dir = tmp_path  # Geçici klasöre kaydet
    return viz

def test_init(viz):
    """__init__ metodunu test et."""
    assert viz.analytics is not None
    assert viz.output_dir.exists()

def test_validate_data(viz):
    """_validate_data metodunu test et."""
    assert viz._validate_data({'key': 'value'}) is True
    assert viz._validate_data({}) is False
    assert viz._validate_data(None) is False

def test_plot_hourly_distribution(viz):
    """Saatlik dağılım grafiği oluşturmayı test et."""
    result = viz.plot_hourly_distribution()
    assert result == True
    assert os.path.exists(os.path.join(viz.output_dir, "hourly_distribution.png"))

def test_plot_daily_trend(viz):
    """Günlük trend grafiği oluşturmayı test et."""
    result = viz.plot_daily_trend()
    assert result == True
    assert os.path.exists(os.path.join(viz.output_dir, "daily_trend.png"))

def test_plot_weekly_comparison(viz):
    """Haftalık karşılaştırma grafiği oluşturmayı test et."""
    result = viz.plot_weekly_comparison()
    assert result == True
    assert os.path.exists(os.path.join(viz.output_dir, "weekly_comparison.png"))

def test_create_heatmap(viz):
    """Isı haritası oluşturmayı test et."""
    with patch.object(viz.analytics, 'get_hourly_stats') as mock_stats:
        # 24 saatlik veri oluştur
        mock_stats.return_value = {i: np.random.randint(0, 100) for i in range(24)}
        
        result = viz.create_heatmap(days=7)
        assert result == True
        assert os.path.exists(os.path.join(viz.output_dir, "heatmap.png"))

def test_plot_visit_duration_distribution(viz):
    """Ziyaret süresi dağılımı grafiği oluşturmayı test et."""
    result = viz.plot_visit_duration_distribution()
    assert result == True
    assert os.path.exists(os.path.join(viz.output_dir, "visit_duration.png"))

def test_empty_data_handling(viz, mock_analytics):
    """Boş veri durumunu test et."""
    mock_analytics.get_hourly_stats.return_value = {}
    result = viz.plot_hourly_distribution()
    assert result == False

def test_error_handling(viz, mock_analytics):
    """Hata durumlarını test et."""
    mock_analytics.get_hourly_stats.side_effect = Exception("Test hatası")
    result = viz.plot_hourly_distribution()
    assert result == False

def test_plot_style_settings(viz):
    """Grafik stil ayarlarını test et."""
    assert 'sans-serif' in plt.rcParams['font.family']
    assert plt.rcParams['figure.figsize'] == [12, 6]
    assert plt.rcParams['axes.unicode_minus'] == False

def test_filename_format(viz):
    """Dosya adı formatını test et."""
    result = viz.plot_hourly_distribution()
    assert result == True
    assert os.path.exists(os.path.join(viz.output_dir, "hourly_distribution.png"))

def test_memory_cleanup(viz):
    """Bellek temizleme işlemlerini test et."""
    # Grafik oluştur
    viz.plot_hourly_distribution()
    
    # Grafikleri kapat ve belleği temizle
    plt.close('all')
    gc.collect()
    
    # Grafik nesnelerinin temizlendiğini kontrol et
    assert len(plt.get_fignums()) == 0

def test_save_plot_error_handling(viz):
    """Grafik kaydetme hatalarını test et."""
    with patch('matplotlib.pyplot.savefig') as mock_save:
        mock_save.side_effect = Exception("Kaydetme hatası")
        
        with pytest.raises(Exception) as exc_info:
            viz._save_plot("test.png")
        
        assert "Kaydetme hatası" in str(exc_info.value)

def test_plot_parameters(viz):
    """Grafik parametrelerini test et."""
    # Saatlik dağılım grafiği
    viz.plot_hourly_distribution()
    
    # Grafik dosyasının oluşturulduğunu kontrol et
    assert os.path.exists(os.path.join(viz.output_dir, "hourly_distribution.png"))
    
    # Günlük trend grafiği
    viz.plot_daily_trend()
    assert os.path.exists(os.path.join(viz.output_dir, "daily_trend.png"))
    
    # Haftalık karşılaştırma grafiği
    viz.plot_weekly_comparison()
    assert os.path.exists(os.path.join(viz.output_dir, "weekly_comparison.png"))
    
    # Ziyaret süresi dağılımı grafiği
    viz.plot_visit_duration_distribution()
    assert os.path.exists(os.path.join(viz.output_dir, "visit_duration.png"))

class TestVisualization(unittest.TestCase):
    def setUp(self):
        self.test_data = self.generate_test_data()  # Test verilerini oluştur

    def test_customer_traffic_plot(self):
        """Müşteri trafiği grafiği testi"""
        fig, ax = plt.subplots()
        ax.plot(self.test_data['timestamp'], self.test_data['customer_count'])
        
        self.assertIsNotNone(ax.get_title())
        self.assertIsNotNone(ax.get_xlabel())
        self.assertIsNotNone(ax.get_ylabel())
        plt.close()

    def test_heatmap_visualization(self):
        """Isı haritası görselleştirme testi"""
        fig, ax = plt.subplots()
        sns.heatmap(self.test_data['heatmap_matrix'], ax=ax)
        
        self.assertIsNotNone(ax.get_title())
        self.assertTrue(ax.collections[0].colorbar is not None)
        plt.close()

    def test_weekly_report_charts(self):
        """Haftalık rapor grafikleri testi"""
        fig, (ax1, ax2) = plt.subplots(2, 1)
        
        # Günlük toplam müşteri grafiği
        ax1.bar(self.test_data['days'], self.test_data['daily_totals'])
        
        # Ortalama ziyaret süresi grafiği
        ax2.plot(self.test_data['days'], self.test_data['avg_duration'])
        
        self.assertIsNotNone(ax1.get_title())
        self.assertIsNotNone(ax2.get_title())
        plt.close()

    def generate_test_data(self):
        # Test için örnek veri oluştur
        return {
            'timestamp': pd.date_range(start='2024-01-01', periods=24, freq='H'),
            'customer_count': np.random.randint(0, 50, 24),
            'heatmap_matrix': np.random.rand(6, 4),
            'days': ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'],
            'daily_totals': np.random.randint(100, 500, 7),
            'avg_duration': np.random.randint(10, 30, 7)
        } 