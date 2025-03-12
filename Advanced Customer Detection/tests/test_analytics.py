import unittest
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

class TestAnalytics(unittest.TestCase):
    def setUp(self):
        # Test verilerini hazırla
        self.test_data = {
            'timestamp': [datetime.now() - timedelta(hours=i) for i in range(24)],
            'customer_count': np.random.randint(0, 50, 24),
            'visit_duration': np.random.randint(1, 60, 24)
        }
        self.df = pd.DataFrame(self.test_data)

    def test_hourly_analysis(self):
        """Saatlik yoğunluk analizi testi"""
        hourly_stats = self.df.groupby(self.df['timestamp'].dt.hour)['customer_count'].mean()
        
        self.assertIsNotNone(hourly_stats)
        self.assertEqual(len(hourly_stats), 24)  # 24 saat için veri olmalı
        self.assertTrue(all(count >= 0 for count in hourly_stats))

    def test_daily_report(self):
        """Günlük rapor testi"""
        daily_stats = self.df.groupby(self.df['timestamp'].dt.date).agg({
            'customer_count': ['sum', 'mean', 'max'],
            'visit_duration': 'mean'
        })
        
        self.assertIsNotNone(daily_stats)
        self.assertTrue(all(daily_stats['customer_count']['sum'] >= 0))

    def test_heatmap_data(self):
        """Isı haritası veri testi"""
        # 24 saatlik veriyi 6x4'lük ısı haritası matrisine dönüştür
        heatmap_data = self.df['customer_count'].values.reshape(6, 4)
        
        self.assertEqual(heatmap_data.shape, (6, 4))
        self.assertTrue(np.all(heatmap_data >= 0))

    def test_visit_duration_analysis(self):
        """Ziyaret süresi analizi testi"""
        duration_stats = {
            'mean': self.df['visit_duration'].mean(),
            'median': self.df['visit_duration'].median(),
            'max': self.df['visit_duration'].max()
        }
        
        self.assertTrue(0 <= duration_stats['mean'] <= 60)
        self.assertTrue(0 <= duration_stats['median'] <= 60)
        self.assertTrue(0 <= duration_stats['max'] <= 60) 