from flask import Flask, render_template
from database import get_db_connection, init_db

app = Flask(__name__)


@app.route("/")
def index():
    # DB에서 모든 의견을 최신순으로 가져와 메인 화면에 표시
    conn = get_db_connection()
    opinions = conn.execute(
        "SELECT * FROM opinions ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return render_template("index.html", opinions=opinions)


if __name__ == "__main__":
    init_db()  # 서버 켤 때 DB 테이블 준비
    app.run(debug=True)
