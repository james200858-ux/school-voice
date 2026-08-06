import sqlite3

DB_NAME = "school_voice.db"


def get_db_connection():
    # DB에 연결하고, 결과를 딕셔너리처럼 다룰 수 있게 설정
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # 서버 시작 시 schema.sql을 읽어서 테이블이 없으면 생성
    conn = get_db_connection()
    with open("schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
