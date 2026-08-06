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
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO opinions (title, content, category) VALUES (?, ?, ?)",
            (title, content, category)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("write.html")


@app.route("/opinion/<int:opinion_id>")
def detail(opinion_id):
    # URL의 opinion_id로 해당 의견 하나만 조회
    conn = get_db_connection()
    opinion = conn.execute(
        "SELECT * FROM opinions WHERE id = ?", (opinion_id,)
    ).fetchone()
    conn.close()
    return render_template("detail.html", opinion=opinion)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", debug=True)
