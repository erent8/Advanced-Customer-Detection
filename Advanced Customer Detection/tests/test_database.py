import unittest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.models import CustomerDetection

class TestDatabase(unittest.TestCase):
    """Veritabanı testleri."""
    
    @classmethod
    def setUpClass(cls):
        """Test veritabanını oluştur."""
        cls.engine = create_engine('sqlite:///database/test_customer_data.db')
        Base.metadata.create_all(cls.engine)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()
    
    def setUp(self):
        """Her test öncesi tabloları temizle."""
        self.session.query(CustomerDetection).delete()
        self.session.commit()
    
    def test_customer_detection_creation(self):
        """Müşteri tespiti oluşturma testi."""
        detection = CustomerDetection(
            timestamp=datetime.now(),
            customer_count=10,
            confidence_score=0.95,
            detection_area="Test Area"
        )
        self.session.add(detection)
        self.session.commit()
        
        saved_detection = self.session.query(CustomerDetection).first()
        self.assertIsNotNone(saved_detection)
        self.assertEqual(saved_detection.customer_count, 10)
        self.assertEqual(saved_detection.detection_area, "Test Area")
    
    def test_customer_detection_query(self):
        """Müşteri tespiti sorgulama testi."""
        # Test verisi ekle
        now = datetime.now()
        detections = [
            CustomerDetection(
                timestamp=now - timedelta(hours=i),
                customer_count=i * 10,
                confidence_score=0.9,
                detection_area="Test Area"
            )
            for i in range(5)
        ]
        self.session.add_all(detections)
        self.session.commit()
        
        # Sorgu testleri
        count = self.session.query(CustomerDetection).count()
        self.assertEqual(count, 5)
        
        latest = self.session.query(CustomerDetection).order_by(
            CustomerDetection.timestamp.desc()
        ).first()
        self.assertEqual(latest.customer_count, 0)
    
    def test_invalid_data(self):
        """Geçersiz veri testi."""
        with self.assertRaises(Exception):
            detection = CustomerDetection(
                timestamp=None,  # timestamp null olamaz
                customer_count=-1,  # negatif sayı olmamalı
                confidence_score=2.0,  # 0-1 arası olmalı
                detection_area=""  # boş olmamalı
            )
            self.session.add(detection)
            self.session.commit()
    
    @classmethod
    def tearDownClass(cls):
        """Test sonrası temizlik."""
        cls.session.close()
        Base.metadata.drop_all(cls.engine)

if __name__ == '__main__':
    unittest.main() 