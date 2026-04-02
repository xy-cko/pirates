from typing import Optional
from datetime import datetime
from sqlalchemy import Integer, Text, TIMESTAMP, func, create_engine
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import create_engine
import os

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

db_url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(db_url)

class Base(DeclarativeBase):
    pass

class RequestsLog(Base):
    __tablename__ = "requests_log"
    
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    sentence: Mapped[Optional[str]] = mapped_column(Text)
    magic_number: Mapped[Optional[int]] = mapped_column(Integer)
    english_output: Mapped[Optional[str]] = mapped_column(Text)
    japanese_output: Mapped[Optional[str]] = mapped_column(Text)
    mongolian_output: Mapped[Optional[str]] = mapped_column(Text)
    error: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now())

def init_db():
    Base.metadata.create_all(bind=engine)