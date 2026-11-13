# 	리뷰 CRUD
from datetime import datetime
from bson import ObjectId

from database.mongo_db import reviews
from services.book_service import get_book


# 1. 리뷰 등록
def insert_review(book_id, reviewer, rating, content):

    # MySQL에서 도서 존재 여부 확인
    book = get_book(book_id)

    if not book:
        print("존재하지 않는 도서입니다.")
        return None

    if not 1 <= rating <= 5:
        print("평점은 1~5점만 가능합니다.")
        return None

    document = {
        "book_id": book_id,
        "reviewer": reviewer,
        "rating": rating,
        "content": content,
        "created_at": datetime.now(),
        "updated_at": None
    }

    result = reviews.insert_one(document)

    return str(result.inserted_id)


# 2. 특정 도서 리뷰 조회
def get_reviews_by_book(book_id):

    return list(
        reviews.find(
            {"book_id": book_id}
        ).sort("created_at", -1)
    )


# 3. 리뷰어별 리뷰 조회
def get_reviews_by_reviewer(reviewer):

    return list(
        reviews.find({
            "reviewer": {
                "$regex": reviewer,
                "$options": "i"
            }
        }).sort("created_at", -1)
    )


# 4. 리뷰 수정
def update_review(review_id, reviewer, rating, content):

    if not 1 <= rating <= 5:
        return False

    try:
        result = reviews.update_one(
            {"_id": ObjectId(review_id)},
            {
                "$set": {
                    "reviewer": reviewer,
                    "rating": rating,
                    "content": content,
                    "updated_at": datetime.now()
                }
            }
        )

        return result.modified_count > 0

    except Exception as e:
        print("리뷰 수정 실패:", e)
        return False


# 5. 리뷰 삭제
def delete_review(review_id):

    try:
        result = reviews.delete_one(
            {"_id": ObjectId(review_id)}
        )

        return result.deleted_count > 0

    except Exception as e:
        print("리뷰 삭제 실패:", e)
        return False


# 6. 도서별 평점 통계
def get_review_stats(book_id):

    pipeline = [
        {
            "$match": {
                "book_id": book_id
            }
        },
        {
            "$group": {
                "_id": "$book_id",
                "avg_rating": {
                    "$avg": "$rating"
                },
                "review_count": {
                    "$sum": 1
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "avg_rating": {
                    "$round": ["$avg_rating", 1]
                },
                "review_count": 1
            }
        }
    ]

    result = list(reviews.aggregate(pipeline))

    if result:
        return result[0]

    return {
        "avg_rating": 0,
        "review_count": 0
    }