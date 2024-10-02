from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Log(Base):
    __tablename__ = 'log'
    
    id = Column(Integer, primary_key=True, index=True)
    user_question = Column(String(500), nullable=False)
    assistant_answer = Column(String(500), nullable=False)
    datetime = Column(DateTime(timezone=True), server_default=func.now())


class Blog(Base):
    __tablename__ = 'Blog'  # MSSQL'deki tablo adı

    id = Column(Integer, primary_key=True, index=True)
    blog_name = Column(String(100), nullable=False)
    context = Column(String(500), nullable=False)
    author = Column(String(50), nullable=False)