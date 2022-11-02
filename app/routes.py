from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, abort, make_response, request

# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description =description
        
# books = [
#     Book(1, "Green Eggs and Ham", "Book about green eggs and ham"),
#     Book(2, "Red Fish, Blue Fish", "Book about fishies"),
#     Book(3, "Pride and Prejudice", "Book about love")
# ]

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["GET"])
def read_all_books():
    title_query = request.args.get("title") #Returns the value of the query param if it was set, or "None" if query param isn't found
    if title_query: #Checks if query param was provided
        books = Book.query.filter_by(title=title_query)
        # print(f"Books = {books}") --- This prints out a SELECT query - interesting
    else:
        books = Book.query.all()

    # books = Book.query.all() #returns list of instances of Book
    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    return jsonify(books_response) #make_response doesn't handle lists

@books_bp.route("", methods=["POST"])
def create_books():
    request_body = request.get_json() #####!!!!!!! FIGURE OUT WHAT THIS DOES
    new_book = Book.from_dict(request_body)
    db.session.add(new_book)
    db.session.commit()
    
    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message": f"book {book_id} invalid"}, 400))

    book = Book.query.get(book_id)
    
    if not book:
        abort(make_response({"message": f"book {book_id} not found"}, 404))

    return book

@books_bp.route("/<book_id>", methods=["GET"]) #GET requests usually don't include a request body
def get_one_book(book_id): #parameter here (book_id) must match route parameter in line above 
    book = validate_book(book_id)
    # book = Book.query.get(book_id) #SQLAL syntax to look for one book, returns an instance of Book #primary key is supposed to be in the (), this one was provied in the route parameter
    return book.to_dict()#Flask will auto. converet a dict into an HTTP response body

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json() #reads the HTTP request body/parses the JSON body into a python dict

    book.title=request_body["title"]
    book.description=request_body["description"]
    # db.session.add()
    db.session.commit() #every time a SQLA model is updated, we want to commit the change to the database using this line
    
    return make_response(jsonify(f"Book #{book.id} successfully updated"), 200)

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)
    
    db.session.delete(book) #Use SQLA's fxns to tell DB to prepare to delete our book
    db.session.commit() #Actually apply our DB changes (of deletion)

    return make_response(jsonify(f"Book #{book_id} successfully deleted")) #Can still access book_id bc variable itslef is stll in app's scope. Object stored in memeory and referenced by book doesn't auto update in response to changes in DB





# @books_bp.route("", methods=["GET"])
# def handle_books():
#     books_response = []
#     for book in books:
#         books_response.append({
#             "id": book.id,
#             "title": book.title,
#             "description": book.description
#         })
#     return jsonify(books_response)


# @books_bp.route("/<book_id>", methods=["GET"])
# def handle_book(book_id):
#     book = validate_book(book_id)
#     print(book)
#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description
#     }