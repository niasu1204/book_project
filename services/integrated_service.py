# MySQL + MongoDB 통합 기능
from database.database import SessionLocal
from database.mongo_db import reviews
from models.book import Book

from services.review_service import (
    get_reviews_by_book,
    get_review_stats
)


# 1. 도서 상세정보 + 리뷰 목록 + 평점
def get_book_detail(book_id):

    with SessionLocal() as session:
        book = session.query(Book)\
            .filter(Book.book_id == book_id)\
            .first()

        if not book:
            return None

        book_data = {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "publisher": book.publisher,
            "price": book.price,
            "category": book.category,
            "stock": book.stock,
            "reg_date": book.reg_date
        }

    book_data["reviews"] = get_reviews_by_book(book_id)

    book_data.update(get_review_stats(book_id))

    return book_data


# 2. 전체 도서 + 리뷰 개수
def get_all_books_with_review_count():

    with SessionLocal() as session:
        books = session.query(Book).all()

        book_list = [
            {
                "book_id": b.book_id,
                "title": b.title,
                "author": b.author,
                "price": b.price,
                "category": b.category
            }
            for b in books
        ]

    # MongoDB에서 도서별 리뷰 개수 집계
    pipeline = [
        {
            "$group": {
                "_id": "$book_id",
                "review_count": {
                    "$sum": 1
                }
            }
        }
    ]

    result = reviews.aggregate(pipeline)

    count_map = {
        row["_id"]: row["review_count"]
        for row in result
    }

    for book in book_list:
        book["review_count"] = count_map.get(
            book["book_id"], 0
        )

    return book_list


# 3. 리뷰가 없는 도서만 삭제
def delete_book_safely(book_id):

    with SessionLocal() as session:
        try:
            book = session.query(Book)\
                .filter(Book.book_id == book_id)\
                .first()

            if not book:
                return "도서를 찾을 수 없습니다."

            # MongoDB에 리뷰가 있는지 확인
            count = reviews.count_documents({
                "book_id": book_id
            })

            if count > 0:
                return "리뷰가 존재하여 삭제할 수 없습니다."

            session.delete(book)
            session.commit()

            return "도서 삭제 완료"

        except Exception as e:
            session.rollback()
            print("삭제 실패:", e)
            return "도서 삭제 실패"