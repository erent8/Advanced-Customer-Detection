from src.database import DatabaseManager
from src.analytics import CustomerAnalytics
from src.dashboard import CustomerDashboard
import traceback
import sys

def main():
    try:
        print("Veritabanı bağlantısı oluşturuluyor...")
        db_manager = DatabaseManager()
        db_manager.init_db()  # Veritabanını başlat
        session = db_manager.SessionLocal()
        
        print("Analytics nesnesi oluşturuluyor...")
        analytics = CustomerAnalytics(session)
        
        print("Dashboard başlatılıyor...")
        dashboard = CustomerDashboard(analytics)
        
        print("\nDashboard hazır! http://127.0.0.1:8050 adresini tarayıcınızda açın.")
        print("Çıkmak için Ctrl+C tuşlarına basın.\n")
        dashboard.run(debug=True, port=8050)
        
    except Exception as e:
        print("\nHATA! Dashboard başlatılırken bir sorun oluştu:")
        print(f"Hata mesajı: {str(e)}")
        print("\nHata detayları:")
        traceback.print_exc()
        
    finally:
        try:
            session.close()
            print("\nVeritabanı bağlantısı kapatıldı.")
        except:
            pass

if __name__ == "__main__":
    main() 