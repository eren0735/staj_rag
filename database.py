# database.py
import os
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLAlchemy Base
Base = declarative_base()

# SQL Server veritabanı bağlantı bilgilerini ayarlayın
server = os.getenv("DB_SERVER", "DESKTOP-MFA8I12")  # veya 'localhost'
database_name = os.getenv("DB_NAME", "blog")
username = os.getenv("DB_USERNAME", "")  # SQL Server kullanıcı adı
password = os.getenv("DB_PASSWORD", "")  # SQL Server şifresi
trusted_connection = os.getenv("DB_TRUSTED_CONNECTION", "yes")

# ODBC bağlantı dizesi
connection_string = (
    f"mssql+pyodbc://{username}:{password}@{server}/{database_name}"
    f"?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection={trusted_connection}"
)

# SQLAlchemy motorunu oluştur
engine = create_engine(connection_string)

# Oturum oluşturucu
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Veritabanı oturumu almak için bir bağımlılık
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Veritabanı tablolarını oluştur
def create_tables():
    Base.metadata.create_all(bind=engine)
