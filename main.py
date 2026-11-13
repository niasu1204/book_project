# 프로그램 시작 및 메인 메뉴
from sqlalchemy import text

from database.database import Base, engine, SessionLocal
from database.mongo_db import client, init_mongo

# ORM 모델을 먼저 import해야 테이블 생성 대상에 등록됨
from models.book import Book

from menus.book_menu import book_menu
from menus.review_menu import review_menu

from services.integrated_service import (
    get_book_detail,
    get_all_books_with_review_count
)


# MySQL 연결 확인
def check_mysql():

    with SessionLocal() as session:
        session.execute(text("SELECT 1"))

    print("MySQL 연결 성공")


# MongoDB 연결 확인
def check_mongodb():

    init_mongo()

    print("MongoDB 연결 성공")


# 1. 도서 상세정보 + 리뷰 통합 조회
def menu_integrated_detail():

    print("\n[도서 상세정보 및 리뷰 통합 조회]")

    try:
        book_id = int(input("도서번호: "))

        if book_id < 1:
            print("도서번호는 1 이상이어야 합니다.")
            return

    except ValueError:
        print("도서번호는 숫자로 입력하세요.")
        return

    data = get_book_detail(book_id)

    if not data:
        print("존재하지 않는 도서입니다.")
        return

    print("\n========== 도서 정보 ==========")
    print(f"도서번호 : {data['book_id']}")
    print(f"도서명   : {data['title']}")
    print(f"저자     : {data['author']}")
    print(f"출판사   : {data['publisher']}")
    print(f"가격     : {data['price']:,}원")
    print(f"카테고리 : {data['category']}")
    print(f"재고     : {data['stock']}권")

    print("\n========== 리뷰 통계 ==========")
    print(f"평균 평점 : {data['avg_rating']}점")
    print(f"리뷰 개수 : {data['review_count']}개")

    print("\n========== 리뷰 목록 ==========")

    if not data["reviews"]:
        print("등록된 리뷰가 없습니다.")

    else:
        for review in data["reviews"]:
            print("-" * 40)
            print(f"리뷰어 : {review['reviewer']}")
            print(f"평점   : {review['rating']}점")
            print(f"내용   : {review['content']}")
            print(f"작성일 : {review['created_at']}")


# 2. 전체 도서 + 리뷰 개수
def menu_all_books_with_count():

    print("\n[전체 도서 및 리뷰 개수]")

    book_list = get_all_books_with_review_count()

    if not book_list:
        print("등록된 도서가 없습니다.")
        return

    for book in book_list:
        print("-" * 50)
        print(f"도서번호 : {book['book_id']}")
        print(f"도서명   : {book['title']}")
        print(f"저자     : {book['author']}")
        print(f"가격     : {book['price']:,}원")
        print(f"카테고리 : {book['category']}")
        print(f"리뷰 개수: {book['review_count']}개")


# 메인 메뉴
def main_menu():

    while True:

        print("""
================================
          도서 관리 시스템
================================

1. 도서 관리
2. 리뷰 관리

3. 도서 상세정보 + 리뷰 조회
4. 전체 도서 + 리뷰 개수 조회

0. 프로그램 종료

================================
""")

        choice = input("메뉴 선택: ").strip()

        if choice == "1":
            book_menu()

        elif choice == "2":
            review_menu()

        elif choice == "3":
            menu_integrated_detail()

        elif choice == "4":
            menu_all_books_with_count()

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("잘못된 메뉴입니다.")


# 프로그램 시작
def main():

    try:
        print("데이터베이스 연결 확인 중...")

        # MySQL 연결 확인
        check_mysql()

        # MongoDB 연결 확인 및 인덱스 생성
        check_mongodb()

        # ORM 테이블 생성
        Base.metadata.create_all(bind=engine)

        print("\n도서 관리 시스템을 시작합니다.")

        main_menu()

    except Exception as e:
        print("\n프로그램 실행 중 오류가 발생했습니다.")
        print(e)

    finally:
        client.close()
        engine.dispose()
        print("데이터베이스 연결을 종료했습니다.")


if __name__ == "__main__":
    main()