#도서 메뉴
from services.book_service import (
    insert_book,
    get_all_books,
    get_book,
    search_books,
    update_book,
    delete_book,
    get_books_by_category,
)


# 숫자 입력 검증
def input_int(prompt, min_value=None):
    while True:
        try:
            value = int(input(prompt))

            if min_value is not None and value < min_value:
                print(f"{min_value} 이상의 숫자를 입력하세요.")
                continue

            return value

        except ValueError:
            print("숫자만 입력하세요.")


# 도서 한 권 출력
def print_book(book):
    print("-" * 50)
    print(f"도서번호 : {book.book_id}")
    print(f"도서명   : {book.title}")
    print(f"저자     : {book.author}")
    print(f"출판사   : {book.publisher}")
    print(f"가격     : {book.price:,}원")
    print(f"카테고리 : {book.category}")
    print(f"재고     : {book.stock}권")
    print(f"등록일   : {book.reg_date}")


# 1. 도서 등록
def menu_insert_book():
    print("\n[도서 등록]")

    title = input("도서명: ").strip()
    author = input("저자: ").strip()
    publisher = input("출판사: ").strip()
    price = input_int("가격: ", 0)
    category = input("카테고리: ").strip()
    stock = input_int("재고: ", 0)

    if not title or not author:
        print("도서명과 저자는 필수 입력 항목입니다.")
        return

    book_id = insert_book(
        title,
        author,
        publisher,
        price,
        category,
        stock
    )

    if book_id:
        print(f"도서 등록 완료! 도서번호: {book_id}")


# 2. 전체 도서 조회
def menu_all_books():
    print("\n[전체 도서 조회]")

    books = get_all_books()

    if not books:
        print("등록된 도서가 없습니다.")
        return

    for book in books:
        print_book(book)


# 3. 도서 상세 조회
def menu_book_detail():
    print("\n[도서 상세 조회]")

    book_id = input_int("도서번호: ", 1)
    book = get_book(book_id)

    if not book:
        print("존재하지 않는 도서입니다.")
        return

    print_book(book)


# 4. 도서명 검색
def menu_search_books():
    print("\n[도서명 검색]")

    keyword = input("검색할 도서명: ").strip()

    books = search_books(keyword)

    if not books:
        print("검색 결과가 없습니다.")
        return

    for book in books:
        print_book(book)


# 5. 도서 수정
def menu_update_book():
    print("\n[도서 정보 수정]")

    book_id = input_int("수정할 도서번호: ", 1)
    book = get_book(book_id)

    if not book:
        print("존재하지 않는 도서입니다.")
        return

    print_book(book)
    print("\n수정하지 않을 항목은 Enter를 누르세요.")

    title = input(f"도서명 [{book.title}]: ").strip()
    author = input(f"저자 [{book.author}]: ").strip()
    publisher = input(f"출판사 [{book.publisher or ''}]: ").strip()
    price = input(f"가격 [{book.price}]: ").strip()
    category = input(f"카테고리 [{book.category or ''}]: ").strip()
    stock = input(f"재고 [{book.stock}]: ").strip()

    # 빈 값이면 기존 값 유지
    title = title or book.title
    author = author or book.author
    publisher = publisher or book.publisher
    category = category or book.category

    try:
        price = int(price) if price else book.price
        stock = int(stock) if stock else book.stock

        if price < 0 or stock < 0:
            print("가격과 재고는 음수일 수 없습니다.")
            return

    except ValueError:
        print("가격과 재고는 숫자로 입력하세요.")
        return

    result = update_book(
        book_id,
        title,
        author,
        publisher,
        price,
        category,
        stock
    )

    print("수정 완료" if result else "수정 실패")


# 6. 도서 삭제
def menu_delete_book():
    print("\n[도서 삭제]")

    book_id = input_int("삭제할 도서번호: ", 1)

    confirm = input("정말 삭제하시겠습니까? (y/n): ")

    if confirm.lower() != "y":
        print("삭제를 취소했습니다.")
        return

    # 리뷰가 있는 도서는 삭제하지 않는 안전한 함수
    from services.integrated_service import delete_book_safely

    result = delete_book_safely(book_id)
    print(result)


# 7. 카테고리별 조회
def menu_category_books():
    print("\n[카테고리별 도서 조회]")

    category = input("카테고리: ").strip()

    books = get_books_by_category(category)

    if not books:
        print("해당 카테고리의 도서가 없습니다.")
        return

    for book in books:
        print_book(book)


# 8. 재고 확인
def menu_check_stock():
    print("\n[도서 재고 확인]")

    book_id = input_int("도서번호: ", 1)
    stock = check_stock(book_id)

    if stock is None:
        print("존재하지 않는 도서입니다.")
    else:
        print(f"현재 재고: {stock}권")


# 도서 관리 메뉴
def book_menu():

    while True:
        print("""
========== 도서 관리 ==========

1. 도서 등록
2. 전체 도서 조회
3. 도서 상세 조회
4. 도서명 검색
5. 도서 정보 수정
6. 도서 삭제
7. 카테고리별 조회

0. 메인 메뉴로 돌아가기

==============================
""")

        choice = input("메뉴 선택: ").strip()

        if choice == "1":
            menu_insert_book()

        elif choice == "2":
            menu_all_books()

        elif choice == "3":
            menu_book_detail()

        elif choice == "4":
            menu_search_books()

        elif choice == "5":
            menu_update_book()

        elif choice == "6":
            menu_delete_book()

        elif choice == "7":
            menu_category_books()

        elif choice == "0":
            break

        else:
            print("잘못된 메뉴입니다.")