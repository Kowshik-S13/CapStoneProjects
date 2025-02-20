from flask import request, Flask, jsonify, Blueprint
from app.models import User
from flask import current_app as app
from flask_httpauth import HTTPBasicAuth
from app import db

main_routes = Blueprint('main_routes', __name__)

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    users = User.query.filter_by(username=username).first()
    if users and users.password == password:
        return username
    return None

@main_routes.route("/", methods=["GET"])
@auth.login_required
def home():
    return "Welcome to the User API"

@main_routes.route("/users", methods=["GET"])
@auth.login_required
def get_users():
    users = User.query.all()
    return jsonify([{"id":user.id,"username":user.username} for user in users])

@main_routes.route("/users/<int:id>", methods=["GET"])
@auth.login_required
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({"id":user.id,"username":user.username})

@main_routes.route("/users", methods=["POST"])
@auth.login_required
def add_user():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    username = data.get('username')
    password = data.get('password')
    id = data.get('id')
    if User.query.get(id):
        return jsonify({"message": "id already exists"}), 400
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@main_routes.route("/users/<int:id>", methods=["PUT"])
@auth.login_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.username = data['username']
    user.password = data['password']
    db.session.commit()
    return jsonify({"message": "User updated"}), 200

@main_routes.route("/users/<int:id>", methods=["DELETE"])
@auth.login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200