from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import get_db_connection, init_db

app = Flask(__name__)


@app.route("/")
def index():
    # 검색어가 있으면 제목에 포함된 것만, 없으면 전체 조회
    keyword = request.args.get("keyword", "")

    conn = get_db_connection()
    if keyword:
        opinions = conn.execute(
            "SELECT * FROM opinions WHERE title LIKE ? ORDER BY created_at DESC",
            (f"%{keyword}%",)
        ).fetchall()
    else:
        opinions = conn.execute(
            "SELECT * FROM opinions ORDER BY created_at DESC"
        ).fetchall()
    conn.close()

    return render_template("index.html", opinions=opinions, keyword=keyword)


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
    conn = get_db_connection()
    opinion = conn.execute(
        "SELECT * FROM opinions WHERE id = ?", (opinion_id,)
    ).fetchone()
    conn.close()
    return render_template("detail.html", opinion=opinion)


@app.route("/like/<int:opinion_id>", methods=["POST"])
def like(opinion_id):
    conn = get_db_connection()
    conn.execute(
        "UPDATE opinions SET likes = likes + 1 WHERE id = ?", (opinion_id,)
    )
    conn.commit()
    updated = conn.execute(
        "SELECT likes FROM opinions WHERE id = ?", (opinion_id,)
    ).fetchone()
    conn.close()
    return jsonify({"likes": updated["likes"]})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", debug=True)
