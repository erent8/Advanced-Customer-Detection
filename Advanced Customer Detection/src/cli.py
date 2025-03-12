import click
from datetime import datetime, timedelta
from tabulate import tabulate
from typing import Dict, Any
import json

from src.database import get_db
from src.analytics import CustomerAnalytics
from src.visualization import CustomerVisualization

def format_table(data: Dict[str, Any], title: str) -> str:
    """Veriyi tablo formatına dönüştür."""
    if not data:
        return "Veri bulunamadı."
        
    if isinstance(data, dict) and isinstance(next(iter(data.values())), dict):
        # İç içe sözlük yapısı
        headers = ['Tarih'] + list(next(iter(data.values())).keys())
        rows = [[k] + list(v.values()) for k, v in data.items()]
    else:
        # Basit sözlük yapısı
        headers = ['Metrik', 'Değer']
        rows = [[k, v] for k, v in data.items()]
    
    return f"\n{title}\n" + tabulate(rows, headers=headers, tablefmt='grid')

@click.group()
def cli():
    """Müşteri Analiz Sistemi CLI"""
    pass

@cli.group()
def show():
    """Veri gösterme komutları."""
    pass

@show.command()
@click.option('--format', '-f', type=click.Choice(['table', 'json']), default='table',
              help='Çıktı formatı')
def hourly(format):
    """Bugünün saatlik müşteri istatistiklerini göster."""
    db = next(get_db())
    analytics = CustomerAnalytics(db)
    
    try:
        stats = analytics.get_hourly_stats()
        
        if format == 'json':
            click.echo(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            click.echo(format_table(stats, "Saatlik Müşteri İstatistikleri"))
    except Exception as e:
        click.echo(click.style(f"Hata: {str(e)}", fg='red'))
    finally:
        db.close()

@show.command()
@click.option('--days', '-d', default=7, help='Kaç günlük rapor')
@click.option('--format', '-f', type=click.Choice(['table', 'json']), default='table',
              help='Çıktı formatı')
def daily(days, format):
    """Günlük müşteri raporunu göster."""
    db = next(get_db())
    analytics = CustomerAnalytics(db)
    
    try:
        start_date = datetime.now() - timedelta(days=days)
        stats = analytics.get_daily_report(start_date)
        
        if format == 'json':
            click.echo(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            click.echo(format_table(stats, f"Son {days} Günün Müşteri Raporu"))
    except Exception as e:
        click.echo(click.style(f"Hata: {str(e)}", fg='red'))
    finally:
        db.close()

@show.command()
@click.option('--format', '-f', type=click.Choice(['table', 'json']), default='table',
              help='Çıktı formatı')
def weekly(format):
    """Haftalık müşteri raporunu göster."""
    db = next(get_db())
    analytics = CustomerAnalytics(db)
    
    try:
        stats = analytics.get_weekly_report()
        
        if format == 'json':
            click.echo(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            click.echo(format_table(stats, "Haftalık Müşteri Raporu"))
    except Exception as e:
        click.echo(click.style(f"Hata: {str(e)}", fg='red'))
    finally:
        db.close()

@show.command()
@click.option('--format', '-f', type=click.Choice(['table', 'json']), default='table',
              help='Çıktı formatı')
def monthly(format):
    """Aylık müşteri raporunu göster."""
    db = next(get_db())
    analytics = CustomerAnalytics(db)
    
    try:
        stats = analytics.get_monthly_report()
        
        if format == 'json':
            click.echo(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            click.echo(format_table(stats, "Aylık Müşteri Raporu"))
    except Exception as e:
        click.echo(click.style(f"Hata: {str(e)}", fg='red'))
    finally:
        db.close()

@show.command()
@click.option('--days', '-d', default=30, help='Kaç günlük veri kullanılsın')
@click.option('--format', '-f', type=click.Choice(['table', 'json']), default='table',
              help='Çıktı formatı')
def peak_hours(days, format):
    """En yoğun saatleri göster."""
    db = next(get_db())
    analytics = CustomerAnalytics(db)
    
    try:
        stats = dict(analytics.get_peak_hours(days))
        
        if format == 'json':
            click.echo(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            click.echo(format_table(stats, f"Son {days} Günün En Yoğun Saatleri"))
    except Exception as e:
        click.echo(click.style(f"Hata: {str(e)}", fg='red'))
    finally:
        db.close()

@show.command()
@click.option('--format', '-f', type=click.Choice(['table', 'json']), default='table',
              help='Çıktı formatı')
def visit_duration(format):
    """Ziyaret süresi istatistiklerini göster."""
    db = next(get_db())
    analytics = CustomerAnalytics(db)
    
    try:
        stats = analytics.get_visit_duration_stats()
        
        if format == 'json':
            click.echo(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            click.echo(format_table(stats, "Ziyaret Süresi İstatistikleri"))
    except Exception as e:
        click.echo(click.style(f"Hata: {str(e)}", fg='red'))
    finally:
        db.close()

@cli.group()
def plot():
    """Görselleştirme komutları."""
    pass

@plot.command(name="hourly-dist")
def plot_hourly():
    """Saatlik müşteri dağılımı grafiği oluştur."""
    db = next(get_db())
    analytics = CustomerAnalytics(db)
    viz = CustomerVisualization(analytics)
    
    try:
        result = viz.plot_hourly_distribution()
        if result.startswith("Hata"):
            click.echo(click.style(result, fg='red'))
        else:
            click.echo(click.style(f"Grafik oluşturuldu: {result}", fg='green'))
    except Exception as e:
        click.echo(click.style(f"Hata: {str(e)}", fg='red'))
    finally:
        db.close()

@plot.command(name="daily-trend")
@click.option('--days', '-d', default=30, help='Kaç günlük veri kullanılsın')
def plot_daily(days):
    """Günlük müşteri trendi grafiği oluştur."""
    db = next(get_db())
    analytics = CustomerAnalytics(db)
    viz = CustomerVisualization(analytics)
    
    try:
        result = viz.plot_daily_trend(days)
        if result.startswith("Hata"):
            click.echo(click.style(result, fg='red'))
        else:
            click.echo(click.style(f"Grafik oluşturuldu: {result}", fg='green'))
    except Exception as e:
        click.echo(click.style(f"Hata: {str(e)}", fg='red'))
    finally:
        db.close()

@plot.command(name="weekly-comp")
def plot_weekly():
    """Haftalık karşılaştırma grafiği oluştur."""
    db = next(get_db())
    analytics = CustomerAnalytics(db)
    viz = CustomerVisualization(analytics)
    
    try:
        result = viz.plot_weekly_comparison()
        if result.startswith("Hata"):
            click.echo(click.style(result, fg='red'))
        else:
            click.echo(click.style(f"Grafik oluşturuldu: {result}", fg='green'))
    except Exception as e:
        click.echo(click.style(f"Hata: {str(e)}", fg='red'))
    finally:
        db.close()

@plot.command()
@click.option('--days', '-d', default=30, help='Kaç günlük veri kullanılsın')
def heatmap(days):
    """Müşteri yoğunluğu ısı haritası oluştur."""
    db = next(get_db())
    analytics = CustomerAnalytics(db)
    viz = CustomerVisualization(analytics)
    
    try:
        result = viz.create_heatmap(days)
        if result.startswith("Hata"):
            click.echo(click.style(result, fg='red'))
        else:
            click.echo(click.style(f"Isı haritası oluşturuldu: {result}", fg='green'))
    except Exception as e:
        click.echo(click.style(f"Hata: {str(e)}", fg='red'))
    finally:
        db.close()

@plot.command(name="visit-dist")
def plot_visit_duration():
    """Ziyaret süresi dağılımı grafiği oluştur."""
    db = next(get_db())
    analytics = CustomerAnalytics(db)
    viz = CustomerVisualization(analytics)
    
    try:
        result = viz.plot_visit_duration_distribution()
        if result.startswith("Hata"):
            click.echo(click.style(result, fg='red'))
        else:
            click.echo(click.style(f"Grafik oluşturuldu: {result}", fg='green'))
    except Exception as e:
        click.echo(click.style(f"Hata: {str(e)}", fg='red'))
    finally:
        db.close()

if __name__ == '__main__':
    cli() 