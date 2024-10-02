from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models  # Log ve Blog modellerini içe aktar
import database
from embeddings import initialize_milvus  # Embeddings modülünü içe aktar
from rag import search_similar_blogs

app = FastAPI()

# Jinja2 şablonlarını yüklemek için
templates = Jinja2Templates(directory="C:/Users/erene/OneDrive/Masaüstü/softtech_staj/templates")

# Veritabanı tablolarını oluştur
database.create_tables()  # Tabloları oluştur

# Milvus'ı başlat
initialize_milvus()  # Milvus'ı başlat

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Log kaydetme API ucu
@app.post("/log/add")
def add_log(user_question: str = Form(...), assistant_answer: str = Form(...), db: Session = Depends(database.get_db)):
    new_log = models.Log(user_question=user_question, assistant_answer=assistant_answer)
    db.add(new_log)  # Veritabanına ekle
    db.commit()  # Değişiklikleri kaydet
    return {"message": "Log başarıyla eklendi."}

@app.get("/logs")
def get_logs(request: Request, db: Session = Depends(database.get_db)):
    db_session = next(db)  # Oturumu al
    all_logs = db_session.query(models.Log).all()  # Tüm logları al
    return templates.TemplateResponse("logs.html", {"request": request, "logs": all_logs})  # Şablona geçir

@app.get("/search")
def search(request: Request, query: str, db: Session = Depends(database.get_db)):
    results = search_similar_blogs(query)  # Milvus'ta arama yap
    return templates.TemplateResponse("search_results.html", {"request": request, "results": results})  # Sonuçları şablona geçir
