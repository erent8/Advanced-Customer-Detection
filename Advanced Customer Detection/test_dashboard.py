from src.analytics import CustomerAnalytics
from src.dashboard import CustomerDashboard
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def main():
    # SQLite veritabanı bağlantısı
    engine = create_engine('sqlite:///database/customer_data.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Analytics ve Dashboard nesnelerini oluştur
    analytics = CustomerAnalytics(session)
    dashboard = CustomerDashboard(analytics)
    
    # Dashboard'u başlat
    print("Dashboard başlatılıyor... http://127.0.0.1:8050 adresini ziyaret edin.")
    dashboard.run(debug=True)

if __name__ == "__main__":
    main() 