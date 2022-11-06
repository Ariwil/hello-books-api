from app import db
from app.models.author import Author
from flask import Blueprint, request, jsonify

authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

#______________________POST____________________________________
@authors_bp.route("", methods=["POST"])
def create_an_author():
    request_body = request.get_json()

    new_author = Author(name=request_body["name"])

    db.session.add(new_author)
    db.session.commit()

    return jsonify(f"Author {new_author.name} successfully created"), 201
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

