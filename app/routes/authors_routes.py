from app import db
from app.models.author import Author
from flask import Blueprint, request, jsonify
from app.models.book import Book
from .books_routes import validate_model
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

#______________________POST____________________________________
@authors_bp.route("", methods=["POST"])
def create_an_author():
    request_body = request.get_json()

    new_author = Author(name=request_body["name"])

    db.session.add(new_author)
    db.session.commit()

    return jsonify(f"Author {new_author.name} successfully created"), 201

@authors_bp.route("/<author_id>/books", methods=["POST"])
def create_book(author_id):
    author = validate_model(Author, author_id)
    request_body = request.get_json()


    new_book = Book(title=request_body["title"],
    description=request_body["description"],
    author=author)

    db.session.add(new_book)
    db.session.commit()

    return jsonify(f"Book {new_book.title} successfully created."), 201


#______________________GET____________________________________
@authors_bp.route("", methods=["GET"])
def get_all_authors():
    authors = Author.query.all()

    author_response = []
    for author in authors:
        author_dict = {
            "id": author.id,
            "name": author.name
        }
        author_response.append(author_dict)
    return jsonify(author_response)

@authors_bp.route("/<author_id>/books", methods=["GET"])
def get_all_books_by_author(author_id):
    author = validate_model(Author, author_id)
    # books_by_author = Author.query.with_parent(Book).filter(Author.id==author_id).all()
    #Post.query.with_parent(py).filter(Post.title != 'Snakes').all()
    response=[]
    for book in author.books:
        book_dict = {
            "title": book.title,
            "description": book.description,
            "author_id": author_id
        }
        response.append(book_dict)

    return jsonify(response)