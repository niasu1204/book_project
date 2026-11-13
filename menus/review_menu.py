# 리뷰 메뉴
from services.review_service import (
    insert_review,
    get_reviews_by_book,
    get_reviews_by_reviewer,
    update_review,
    delete_review,
    get_review_stats
)


def input_int(prompt, min_value=None, max_value=None):

    while True:
        try:
            value = int(input(prompt))

            if min_value is not None and value < min_value:
                print(f"{min_value} 이상 입력하세요.")
                continue

            if max_value is not None and value > max_value:
                print(f"{max_value} 이하 입력하세요.")
                continue

            return value

        except ValueError:
            print("숫자만 입력하세요.")


# 리뷰 출력
def print_review(review):

    print("-" * 50)
    print(f"리뷰 ID : {review['_id']}")
    print(f"도서번호: {review['book_id']}")
    print(f"리뷰어  : {review['reviewer']}")
    print(f"평점    : {review['rating']}점")
    print(f"내용    : {review['content']}")
    print(f"작성일  : {review['created_at']}")

    if review.get("updated_at"):
        print(f"수정일  : {review['updated_at']}")


# 1. 리뷰 등록
def menu_insert_review():

    print("\n[리뷰 등록]")

    book_id = input_int("도서번호: ", 1)
    reviewer = input("리뷰어 이름: ").strip()
    rating = input_int("평점 (1~5): ", 1, 5)
    content = input("리뷰 내용: ").strip()

    if not reviewer or not content:
        print("리뷰어와 리뷰 내용은 필수입니다.")
        return

    review_id = insert_review(
        book_id,
        reviewer,
        rating,
        content
    )

    if review_id:
        print("리뷰 등록 완료!")
        print("리뷰 ID:", review_id)


# 2. 도서별 리뷰 조회
def menu_reviews_by_book():

    print("\n[도서별 리뷰 조회]")

    book_id = input_int("도서번호: ", 1)

    review_list = get_reviews_by_book(book_id)

    if not review_list:
        print("등록된 리뷰가 없습니다.")
        return

    for review in review_list:
        print_review(review)


# 3. 리뷰어별 리뷰 조회
def menu_reviews_by_reviewer():

    print("\n[리뷰어별 리뷰 조회]")

    reviewer = input("리뷰어 이름 검색: ").strip()

    if not reviewer:
        print("검색어를 입력하세요.")
        return

    review_list = get_reviews_by_reviewer(reviewer)

    if not review_list:
        print("검색 결과가 없습니다.")
        return

    for review in review_list:
        print_review(review)


# 4. 리뷰 수정
def menu_update_review():

    print("\n[리뷰 수정]")

    review_id = input("수정할 리뷰 ID: ").strip()

    reviewer = input("리뷰어 이름: ").strip()
    rating = input_int("평점 (1~5): ", 1, 5)
    content = input("리뷰 내용: ").strip()

    if not reviewer or not content:
        print("리뷰어와 리뷰 내용은 필수입니다.")
        return

    result = update_review(
        review_id,
        reviewer,
        rating,
        content
    )

    print("수정 완료" if result else "수정 실패")


# 5. 리뷰 삭제
def menu_delete_review():

    print("\n[리뷰 삭제]")

    review_id = input("삭제할 리뷰 ID: ").strip()

    confirm = input("정말 삭제하시겠습니까? (y/n): ")

    if confirm.lower() != "y":
        print("삭제를 취소했습니다.")
        return

    result = delete_review(review_id)

    print("삭제 완료" if result else "삭제 실패")


# 6. 도서별 평점 통계
def menu_review_stats():

    print("\n[도서별 평점 통계]")

    book_id = input_int("도서번호: ", 1)

    stats = get_review_stats(book_id)

    print(f"평균 평점 : {stats['avg_rating']}점")
    print(f"리뷰 개수 : {stats['review_count']}개")


# 리뷰 관리 메뉴
def review_menu():

    while True:
        print("""
========== 리뷰 관리 ==========

1. 리뷰 등록
2. 도서별 리뷰 조회
3. 리뷰어별 리뷰 조회
4. 리뷰 수정
5. 리뷰 삭제
6. 도서별 평점 통계

0. 메인 메뉴로 돌아가기

==============================
""")

        choice = input("메뉴 선택: ").strip()

        if choice == "1":
            menu_insert_review()

        elif choice == "2":
            menu_reviews_by_book()

        elif choice == "3":
            menu_reviews_by_reviewer()

        elif choice == "4":
            menu_update_review()

        elif choice == "5":
            menu_delete_review()

        elif choice == "6":
            menu_review_stats()

        elif choice == "0":
            break

        else:
            print("잘못된 메뉴입니다.")