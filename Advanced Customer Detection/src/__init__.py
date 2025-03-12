"""Müşteri tespit sistemi modülü."""

from .database import init_db
from .logger import log_startup
from .config import config, AppConfig as Config

__version__ = "2.0.0"

def initialize_app():
    """Uygulamayı başlat ve gerekli ayarları yap."""
    # Konfigürasyonu doğrula
    config = Config()
    config.validate()
    
    # Veritabanını başlat
    init_db()
    
    # Başlangıç logunu yaz
    log_startup()
    
    return config 