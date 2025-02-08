import pytest
from click.testing import CliRunner
from unittest.mock import Mock, patch
import json

from src.cli import cli, show, plot
from src.analytics import CustomerAnalytics
from src.visualization import CustomerVisualization

@pytest.fixture
def runner():
    """Click test runner oluştur."""
    return CliRunner()

@pytest.fixture
def mock_analytics():
    """Mock CustomerAnalytics nesnesi oluştur."""
    analytics = Mock(spec=CustomerAnalytics)
    
    # Test verileri
    analytics.get_hourly_stats.return_value = {0: 10, 1: 15}
    analytics.get_daily_report.return_value = {
        '2024-02-01': {'toplam_musteri': 100, 'ortalama_musteri': 10}
    }
    analytics.get_weekly_report.return_value = {
        'Hafta_01': {'toplam_musteri': 500, 'ortalama_musteri': 71.4}
    }
    analytics.get_monthly_report.return_value = {
        '2024-02': {'toplam_musteri': 2000, 'ortalama_musteri': 64.5}
    }
    analytics.get_peak_hours.return_value = [(14, 50), (13, 45)]
    analytics.get_visit_duration_stats.return_value = {
        'ortalama_sure': 300,
        'minimum_sure': 60
    }
    
    return analytics

@pytest.fixture
def mock_viz():
    """Mock CustomerVisualization nesnesi oluştur."""
    viz = Mock(spec=CustomerVisualization)
    
    # Test sonuçları
    viz.plot_hourly_distribution.return_value = "/path/to/hourly.png"
    viz.plot_daily_trend.return_value = "/path/to/daily.png"
    viz.plot_weekly_comparison.return_value = "/path/to/weekly.png"
    viz.create_heatmap.return_value = "/path/to/heatmap.png"
    viz.plot_visit_duration_distribution.return_value = "/path/to/duration.png"
    
    return viz

def test_show_hourly(runner, mock_analytics):
    """'show hourly' komutunu test et."""
    with patch('src.cli.CustomerAnalytics', return_value=mock_analytics):
        # Tablo formatı
        result = runner.invoke(cli, ['show', 'hourly'])
        assert result.exit_code == 0
        assert "Saatlik Müşteri İstatistikleri" in result.output
        
        # JSON formatı
        result = runner.invoke(cli, ['show', 'hourly', '--format', 'json'])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data == {"0": 10, "1": 15}

def test_show_daily(runner, mock_analytics):
    """'show daily' komutunu test et."""
    with patch('src.cli.CustomerAnalytics', return_value=mock_analytics):
        result = runner.invoke(cli, ['show', 'daily', '--days', '7'])
        assert result.exit_code == 0
        assert "Son 7 Günün Müşteri Raporu" in result.output

def test_show_weekly(runner, mock_analytics):
    """'show weekly' komutunu test et."""
    with patch('src.cli.CustomerAnalytics', return_value=mock_analytics):
        result = runner.invoke(cli, ['show', 'weekly'])
        assert result.exit_code == 0
        assert "Haftalık Müşteri Raporu" in result.output

def test_show_monthly(runner, mock_analytics):
    """'show monthly' komutunu test et."""
    with patch('src.cli.CustomerAnalytics', return_value=mock_analytics):
        result = runner.invoke(cli, ['show', 'monthly'])
        assert result.exit_code == 0
        assert "Aylık Müşteri Raporu" in result.output

def test_show_peak_hours(runner, mock_analytics):
    """'show peak-hours' komutunu test et."""
    with patch('src.cli.CustomerAnalytics', return_value=mock_analytics):
        result = runner.invoke(cli, ['show', 'peak-hours'])
        assert result.exit_code == 0
        assert "En Yoğun Saatleri" in result.output

def test_show_visit_duration(runner, mock_analytics):
    """'show visit-duration' komutunu test et."""
    with patch('src.cli.CustomerAnalytics', return_value=mock_analytics):
        result = runner.invoke(cli, ['show', 'visit-duration'])
        assert result.exit_code == 0
        assert "Ziyaret Süresi İstatistikleri" in result.output

def test_plot_hourly_dist(runner, mock_analytics, mock_viz):
    """'plot hourly-dist' komutunu test et."""
    with patch('src.cli.CustomerAnalytics', return_value=mock_analytics), \
         patch('src.cli.CustomerVisualization', return_value=mock_viz):
        result = runner.invoke(cli, ['plot', 'hourly-dist'])
        assert result.exit_code == 0
        assert "Grafik oluşturuldu" in result.output

def test_plot_daily_trend(runner, mock_analytics, mock_viz):
    """'plot daily-trend' komutunu test et."""
    with patch('src.cli.CustomerAnalytics', return_value=mock_analytics), \
         patch('src.cli.CustomerVisualization', return_value=mock_viz):
        result = runner.invoke(cli, ['plot', 'daily-trend', '--days', '30'])
        assert result.exit_code == 0
        assert "Grafik oluşturuldu" in result.output

def test_plot_weekly_comp(runner, mock_analytics, mock_viz):
    """'plot weekly-comp' komutunu test et."""
    with patch('src.cli.CustomerAnalytics', return_value=mock_analytics), \
         patch('src.cli.CustomerVisualization', return_value=mock_viz):
        result = runner.invoke(cli, ['plot', 'weekly-comp'])
        assert result.exit_code == 0
        assert "Grafik oluşturuldu" in result.output

def test_plot_heatmap(runner, mock_analytics, mock_viz):
    """'plot heatmap' komutunu test et."""
    with patch('src.cli.CustomerAnalytics', return_value=mock_analytics), \
         patch('src.cli.CustomerVisualization', return_value=mock_viz):
        result = runner.invoke(cli, ['plot', 'heatmap', '--days', '30'])
        assert result.exit_code == 0
        assert "Isı haritası oluşturuldu" in result.output

def test_plot_visit_dist(runner, mock_analytics, mock_viz):
    """'plot visit-dist' komutunu test et."""
    with patch('src.cli.CustomerAnalytics', return_value=mock_analytics), \
         patch('src.cli.CustomerVisualization', return_value=mock_viz):
        result = runner.invoke(cli, ['plot', 'visit-dist'])
        assert result.exit_code == 0
        assert "Grafik oluşturuldu" in result.output

def test_error_handling(runner, mock_analytics):
    """Hata durumlarını test et."""
    mock_analytics.get_hourly_stats.side_effect = Exception("Test hatası")
    
    with patch('src.cli.CustomerAnalytics', return_value=mock_analytics):
        result = runner.invoke(cli, ['show', 'hourly'])
        assert result.exit_code == 0
        assert "Hata" in result.output 