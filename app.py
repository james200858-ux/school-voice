from flask import Flask, render_template, request, redirect, url_for
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


@app.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "POST":
        # 폼에서 입력받은 데이터 가져오기
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]

        # DB에 새 의견 저장
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO opinions (title, content, category) VALUES (?, ?, ?)",
            (title, content, category)
        )
        conn.commit()
        conn.close()

        # 저장 후 메인 화면으로 이동
        return redirect(url_for("index"))

    # GET 요청이면 등록 폼 화면 보여주기
    return render_template("write.html")


if __name__ == "__main__":
    init_db()  # 서버 켤 때 DB 테이블 준비
    app.run(host="0.0.0.0", debug=True)
