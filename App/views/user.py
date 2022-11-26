from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required
# for exceptions
import sys

from App.controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
    create_author,
    get_all_authors_json
)

# from App.controllers import *   

user_views = Blueprint('user_views', __name__, template_folder='../templates')


# view to be removed or changed
@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users')
def client_app():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/signup', methods=["POST"])
def create_user_route():
    data = request.get_json()
    if not data:
        return "Missing request body.", 400
        
    try:
        new_author = create_author(data['name'], data['dob'], data['qualifications'])
    except Exception as e:
        return f'Could not create due to exception: {e.__class__}', 400 
    new_author = new_author.toJSON()

    username = data['username']
    password = data['password']
    if not username or not password:
        return "Missing username or password parameter.", 400
    
    user = create_user(username, password, new_author['id'])
    if not user:
        return "Failed to create.", 400
    return user.toJSON(), 201
    