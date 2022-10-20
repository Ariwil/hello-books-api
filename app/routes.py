from flask import Blueprint

hello_world_bp = Blueprint("hello_world", __name__)

@hello_world_bp.route("/hello-world", methods=["GET"])
def say_hello_world():
    response_body = "Hello, World!"
    return response_body

@hello_world_bp.route("/hello/JSON", methods=["GET"])
def say_hello_json():
    response_body = {
        "name": "Ariel Wilson",
        "message": "Hello!",
        "hobbies": ["Painting", "Sleeping", "Watching TV"]
    }
    return response_body