from fastapi import FastAPI
from .database import engine
from . import models
from . import rag  # sadece rag modülünü içe aktar

# FastAPI uygulamasını başlat
app = FastAPI()

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

# Yönlendirmeleri ekle
app.include_router(rag.router)  # sadece rag yönlendirmesini ekle

# Ana sayfa
@app.get("/")
def root():
    return {"message": "RAG Servisi"}  # Blog ifadesini kaldırdık
