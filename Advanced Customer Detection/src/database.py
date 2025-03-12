from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
from typing import Generator
import sys

# Src klasörünü Python path'ine ekle
sys.path.append(str(Path(__file__).parent.parent))

Base = declarative_base()

class DatabaseManager:
    """Veritabanı yönetim sınıfı."""
    
    def __init__(self):
        self.db_path = Path(__file__).parent.parent / "database" / "customer_data.db"
        self.db_url = f"sqlite:///{self.db_path}"
        self.engine = create_engine(
            self.db_url, 
            connect_args={"check_same_thread": False}
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine
        )

    def get_db(self) -> Generator:
        """Veritabanı bağlantısı için context manager."""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def init_db(self) -> None:
        """Veritabanını başlat ve tabloları oluştur."""
        import src.models  # Circular import'u önlemek için local import
        Base.metadata.create_all(bind=self.engine)

# Singleton instance
db_manager = DatabaseManager()
get_db = db_manager.get_db
init_db = db_manager.init_db

if __name__ == "__main__":
    print("Veritabanı tabloları oluşturuluyor...")
    init_db()
    print("Veritabanı başarıyla oluşturuldu!") 