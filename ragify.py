from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models
from .. import database
from ..embeddings import search_similar_blogs  # embeddings.py'dan fonksiyonu içe aktar

router = APIRouter()

@router.post("/search/")
def search_blog(query: str, db: Session = Depends(database.get_db)):
    # En benzer blog ID'lerini bul
    similar_blog_ids = search_similar_blogs(query)
    
    if not similar_blog_ids:
        raise HTTPException(status_code=404, detail="No similar blogs found")

    # Bulunan blogları veritabanından al
    similar_blogs = db.query(models.Blog).filter(models.Blog.id.in_(similar_blog_ids)).all()
    
    response = [
        {
            "blog_name": blog.blog_name,
            "author": blog.author,
            "context": blog.context,
        }
        for blog in similar_blogs
    ]
    
    return response
