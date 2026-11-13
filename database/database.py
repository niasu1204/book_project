# SQLAlchemy 연결 및 세션 관리
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:"
    f"{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}:"
    f"{os.getenv('MYSQL_PORT')}/"
    f"{os.getenv('MYSQL_DATABASE')}?charset=utf8mb4"
)

# DB 연결 관리
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

# 세션 생성기
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

# ORM 모델의 부모 클래스
Base = declarative_base()