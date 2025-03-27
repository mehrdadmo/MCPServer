from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class QueryHistory(Base):
    __tablename__ = 'query_history'
    
    id = Column(String, primary_key=True)
    prompt = Column(String)
    response = Column(String)
    timestamp = Column(DateTime) 