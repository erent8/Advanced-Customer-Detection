from loguru import logger
from typing import Optional, Dict, Any
from pathlib import Path
import sys
import json

class LogManager:
    """Log yönetim sınıfı."""
    
    def __init__(self):
        self.log_dir = Path(__file__).parent.parent / "logs"
        self.log_dir.mkdir(exist_ok=True)
        
        # Farklı log dosyaları için yapılandırma
        self._configure_loggers()
    
    def _configure_loggers(self) -> None:
        """Logger'ları yapılandır."""
        # Mevcut logger'ları temizle
        logger.remove()
        
        # Uygulama logları
        logger.add(
            self.log_dir / "app.log",
            rotation="1 day",
            retention="30 days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            level="INFO",
            encoding="utf-8",
            filter=lambda record: record["extra"].get("type") == "app"
        )
        
        # Performans logları
        logger.add(
            self.log_dir / "performance.log",
            rotation="1 day",
            retention="30 days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            level="INFO",
            encoding="utf-8",
            filter=lambda record: record["extra"].get("type") == "performance"
        )
        
        # Hata logları
        logger.add(
            self.log_dir / "error.log",
            rotation="1 day",
            retention="30 days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            level="ERROR",
            encoding="utf-8",
            filter=lambda record: record["level"].name == "ERROR"
        )
        
        # Konsol çıktısı
        logger.add(
            sys.stdout,
            format="<level>{level}</level> | {message}",
            level="INFO",
            colorize=True
        )
        
        # Özel log seviyesi
        logger.level("CUSTOMER", no=25, color="<yellow>")
        logger.level("PERFORMANCE", no=15, color="<cyan>")
    
    def log_customer_detection(self, count: int, confidence: Optional[float] = None) -> None:
        """Müşteri tespitlerini logla."""
        with logger.contextualize(type="app"):
            if confidence:
                logger.log("CUSTOMER", f"Tespit edilen müşteri sayısı: {count} (Güven: {confidence:.2f})")
            else:
                logger.log("CUSTOMER", f"Tespit edilen müşteri sayısı: {count}")
    
    def log_performance_metrics(self, metrics: Dict[str, Any]) -> None:
        """Performans metriklerini logla."""
        with logger.contextualize(type="performance"):
            logger.log("PERFORMANCE", f"Performance metrics: {json.dumps(metrics, indent=2)}")
    
    def log_function_performance(self, func_name: str, execution_time: float, memory_used: float) -> None:
        """Fonksiyon performansını logla."""
        with logger.contextualize(type="performance"):
            logger.log(
                "PERFORMANCE",
                f"Function: {func_name}, Execution time: {execution_time:.2f}s, Memory used: {memory_used:.2f}MB"
            )
    
    def log_error(self, error: Exception, context: Optional[Dict] = None) -> None:
        """Hataları logla."""
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {}
        }
        logger.error(f"Error occurred: {json.dumps(error_info, indent=2)}")
    
    def log_startup(self) -> None:
        """Uygulama başlangıcını logla."""
        with logger.contextualize(type="app"):
            logger.info("Uygulama başlatıldı")
    
    def log_shutdown(self) -> None:
        """Uygulama kapanışını logla."""
        with logger.contextualize(type="app"):
            logger.info("Uygulama kapatıldı")

# Singleton instance
log_manager = LogManager()

# Kolay erişim için fonksiyonlar
log_customer_detection = log_manager.log_customer_detection
log_performance = log_manager.log_performance_metrics
log_function = log_manager.log_function_performance
log_error = log_manager.log_error
log_startup = log_manager.log_startup
log_shutdown = log_manager.log_shutdown 