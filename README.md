1. 파일 압축 출고
2. vscode에서 book_project 위치로 폴더 열기
3. 터미널 열고 위치 확인(book_project)
4. python -m venv venv
5. venv\Scripts\activate
6. pip install sqlalchemy pymysql pymongo python-dotenv
7. .env파일에 db 정보 입력
8. main.py실행

book_project/
│
├── venv/  # 가상환경
│
├── database/
│   ├── mysql_db.py
│   └── mongo_db.py
│
├── services/
│   ├── book_service.py
│   └── review_service.py
│
├── menus/
│   ├── book_menu.py
│   └── review_menu.py
│
├── .env
├── .gitignore
└── main.py
