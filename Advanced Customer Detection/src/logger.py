from loguru import logger
from typing import Optional
from pathlib import Path

class LogManager:
    """Log yönetim sınıfı."""
    
    def __init__(self):
        self.log_path = Path(__file__).parent.parent / "logs" / "app.log"
        self._configure_logger()
    
    def _configure_logger(self) -> None:
        """Logger'ı yapılandır."""
        logger.add(
            self.log_path,
            rotation="1 day",
            retention="30 days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            level="INFO",
            encoding="utf-8"
        )
        logger.level("CUSTOMER", no=25, color="<yellow>")
    
    def log_customer_detection(self, count: int, confidence: Optional[float] = None) -> None:
        """Müşteri tespitlerini logla."""
        if confidence:
            logger.log("CUSTOMER", f"Tespit edilen müşteri sayısı: {count} (Güven: {confidence:.2f})")
        else:
            logger.log("CUSTOMER", f"Tespit edilen müşteri sayısı: {count}")
    
    def log_error(self, error: Exception) -> None:
        """Hataları logla."""
        logger.error(f"Hata oluştu: {str(error)}")
    
    def log_startup(self) -> None:
        """Uygulama başlangıcını logla."""
        logger.info("Uygulama başlatıldı")
    
    def log_shutdown(self) -> None:
        """Uygulama kapanışını logla."""
        logger.info("Uygulama kapatıldı")

# Singleton instance
log_manager = LogManager()
log_customer_detection = log_manager.log_customer_detection
log_error = log_manager.log_error
log_startup = log_manager.log_startup
log_shutdown = log_manager.log_shutdown 