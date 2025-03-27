import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def api_status():
    return jsonify(
        {
            "status": "active",
            "message": "Book Recommendation API is running",
            "version": "1.0.0",
        }
    )


@app.route("/books", methods=["GET"])
def get_books():
    search_query = request.args.get("query")

    if not search_query:
        return jsonify({"error": "Silakan ajukan pencarian!"}), 400

    try:
        response = requests.get(f"http://openlibrary.org/search.json?q={search_query}")
        data = response.json()

        books = []
        for doc in data.get("docs", [])[:5]:
            books.append(
                {
                    "title": doc.get("title"),
                    "author": doc.get("author_name", ["Unknown"])[0],
                    "publish_year": doc.get("first_publish_year"),
                    "isbn": doc.get("isbn", [""])[0],
                }
            )

        return jsonify({"count": len(books), "query": search_query, "results": books})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
