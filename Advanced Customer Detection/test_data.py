from datetime import datetime, timedelta
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import CustomerDetection, Base
import numpy as np

def create_sample_data():
    """Gerçekçi örnek müşteri verileri oluştur."""
    engine = create_engine('sqlite:///database/customer_data.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Mevcut verileri temizle
    session.query(CustomerDetection).delete()
    session.commit()
    
    # Son 30 günlük veri oluştur
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    current_date = start_date
    
    # Saatlik yoğunluk profilleri
    weekday_profile = {
        6: 0.1,   # 06:00
        7: 0.2,   # 07:00
        8: 0.4,   # 08:00
        9: 0.6,   # 09:00
        10: 0.8,  # 10:00
        11: 0.9,  # 11:00
        12: 1.0,  # 12:00
        13: 0.95, # 13:00
        14: 0.85, # 14:00
        15: 0.8,  # 15:00
        16: 0.85, # 16:00
        17: 0.9,  # 17:00
        18: 1.0,  # 18:00
        19: 0.9,  # 19:00
        20: 0.7,  # 20:00
        21: 0.5,  # 21:00
        22: 0.3   # 22:00
    }
    
    weekend_profile = {
        10: 0.4,  # 10:00
        11: 0.6,  # 11:00
        12: 0.8,  # 12:00
        13: 1.0,  # 13:00
        14: 0.95, # 14:00
        15: 0.9,  # 15:00
        16: 0.85, # 16:00
        17: 0.8,  # 17:00
        18: 0.75, # 18:00
        19: 0.7,  # 19:00
        20: 0.5,  # 20:00
        21: 0.3,  # 21:00
        22: 0.2   # 22:00
    }
    
    areas = ["Ana Giriş", "Kasa Bölgesi", "Mağaza İçi", "Çıkış"]
    
    while current_date <= end_date:
        is_weekend = current_date.weekday() >= 5
        profile = weekend_profile if is_weekend else weekday_profile
        base_customers = random.randint(80, 120) if is_weekend else random.randint(100, 150)
        
        for hour, factor in profile.items():
            # Rastgele dalgalanma ekle
            variation = random.uniform(0.8, 1.2)
            customer_count = int(base_customers * factor * variation)
            
            detection = CustomerDetection(
                timestamp=current_date.replace(hour=hour, minute=random.randint(0, 59)),
                customer_count=customer_count,
                confidence_score=random.uniform(0.85, 0.99),
                detection_area=random.choice(areas)
            )
            session.add(detection)
        
        current_date += timedelta(days=1)
    
    session.commit()
    session.close()

if __name__ == "__main__":
    create_sample_data()
    print("Örnek veriler başarıyla oluşturuldu!") 