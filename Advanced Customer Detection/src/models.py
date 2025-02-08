from sqlalchemy import Column, Integer, DateTime, String, Float
from datetime import datetime
import sys
from pathlib import Path

# Src klasörünü Python path'ine ekle
sys.path.append(str(Path(__file__).parent.parent))

from src.database import Base

class CustomerDetection(Base):
    """Müşteri tespitlerini kaydeden model."""
    __tablename__ = 'customer_detections'

    id: int = Column(Integer, primary_key=True)
    timestamp: datetime = Column(DateTime, nullable=False)
    customer_count: int = Column(Integer, nullable=False)
    confidence_score: float = Column(Float)
    detection_area: str = Column(String)  # Kameranın hangi bölgeyi izlediği
    
    def __repr__(self) -> str:
        return f"<CustomerDetection(timestamp={self.timestamp}, count={self.customer_count})>"

    @property
    def to_dict(self) -> dict:
        """Model verilerini sözlük olarak döndür."""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'customer_count': self.customer_count,
            'confidence_score': self.confidence_score,
            'detection_area': self.detection_area
        } 