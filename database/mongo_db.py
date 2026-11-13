# MongoDB 연결
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client[os.getenv("MONGO_DATABASE")]

reviews = db["reviews"]


def init_mongo():
    # 검색 성능을 위한 인덱스
    reviews.create_index("book_id")
    reviews.create_index("reviewer")

    # MongoDB 연결 확인
    client.admin.command("ping")