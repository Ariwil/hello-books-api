from flask import Blueprint, jsonify

# hello_world_bp = Blueprint("hello_world", __name__)

# @hello_world_bp.route("/hello-world", methods=["GET"])
# def say_hello_world():
#     response_body = "Hello, World!"
#     return response_body

# @hello_world_bp.route("/hello/JSON", methods=["GET"])
# def say_hello_json():
#     response_body = {
#         "name": "Ariel Wilson",
#         "message": "Hello!",
#         "hobbies": ["Painting", "Sleeping", "Watching TV"]
#     }
#     return response_body

# @hello_world_bp.route("/broken-endpoint-with-broken-server-code", methods=["GET"])
# def broken_endpoint():
#     response_body = {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }
#     new_hobby = "Surfing"
#     response_body["hobbies"].append(new_hobby)
#     return response_body

class Book():
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description =description
books = [
    Book(1, "Green Eggs and Ham", "Book about green eggs and ham"),
    Book(2, "Red Fish, Blue Fish", "Book about fishies"),
    Book(3, "Pride and Prejudice", "Book about love")
]

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["GET"])
def handle_books():
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["GET"])
def handle_book(book_id):
    book_id = int(book_id)
    for book in books:
        if book.id == book_id:
            return {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
    