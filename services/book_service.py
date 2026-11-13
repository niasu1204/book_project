# 도서 CRUD
from database.database import SessionLocal
from models.book import Book


# 1. 도서 등록
def insert_book(title, author, publisher, price, category, stock):

    with SessionLocal() as session:
        try:
            book = Book(
                title=title,
                author=author,
                publisher=publisher,
                price=price,
                category=category,
                stock=stock
            )

            session.add(book)
            session.commit()
            session.refresh(book)

            return book.book_id

        except Exception as e:
            session.rollback()
            print("도서 등록 실패:", e)
            return None


# 2. 전체 도서 조회
def get_all_books():

    with SessionLocal() as session:
        return session.query(Book)\
            .order_by(Book.book_id)\
            .all()


# 3. 도서 상세 조회
def get_book(book_id):

    with SessionLocal() as session:
        return session.query(Book)\
            .filter(Book.book_id == book_id)\
            .first()


# 4. 도서명 검색
def search_books(keyword):

    with SessionLocal() as session:
        return session.query(Book)\
            .filter(Book.title.like(f"%{keyword}%"))\
            .order_by(Book.book_id)\
            .all()


# 5. 도서 정보 수정
def update_book(book_id, title, author, publisher,
                price, category, stock):

    with SessionLocal() as session:
        try:
            book = session.query(Book)\
                .filter(Book.book_id == book_id)\
                .first()

            if not book:
                return False

            book.title = title
            book.author = author
            book.publisher = publisher
            book.price = price
            book.category = category
            book.stock = stock

            session.commit()

            return True

        except Exception as e:
            session.rollback()
            print("도서 수정 실패:", e)
            return False


# 6. 도서 삭제
def delete_book(book_id):

    with SessionLocal() as session:
        try:
            book = session.query(Book)\
                .filter(Book.book_id == book_id)\
                .first()

            if not book:
                return False

            session.delete(book)
            session.commit()

            return True

        except Exception as e:
            session.rollback()
            print("도서 삭제 실패:", e)
            return False


# 7. 카테고리별 조회
def get_books_by_category(category):

    with SessionLocal() as session:
        return session.query(Book)\
            .filter(Book.category == category)\
            .all()
