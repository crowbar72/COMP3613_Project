from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required


from App.controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
)

from App.controllers import *

user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users')
def client_app():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/static/users')
def static_user_page():
  return send_from_directory('static', 'static-user.html')


@user_views.route('/publications', methods=["GET"])
def get_publications():
    args = request.args
    if not args:
        pubs = get_all_publications_json()
        return jsonify(pubs)
    author_id = args.get("author")
    query = args.get("query")
    pubs = []
    if author_id:
        pubs = get_author_publications(author_id)
    if query:
        query = query.lower()
        print(query)
        pubs = filter(lambda pub: query in pub['title'].lower(), pubs)
    return jsonify(list(pubs))
        

@user_views.route('/publications', methods=["POST"])
def post_publication():
    data = request.get_json()
    author_names = data['authors']
    coauthor_names = data['coauthors']
    authors = sum ( [get_author_by_name(name) for name in author_names], [] )
    coauthors = sum ( [get_author_by_name(name) for name in coauthor_names], [] )
    # return jsonify(author_names)
    new_pub = create_publication(data['title'], authors, coauthors)
    return f'{new_pub.title} was created.', 200

@user_views.route('/author', methods=["POST"])
def create_author_profile():
    data = request.get_json()
    # return jsonify(data)
    new_author = create_author(data['name'], data['dob'], data['qualifications'])
    return f'{new_author.name} was created.', 200

@user_views.route('/author', methods=["GET"])
def get_author_profile():
    authors = get_all_authors_json()
    return jsonify(authors)

@user_views.route('/pubtree', methods=['GET'])
def get_pub_tree():
    args = request.args
    author_id = args.get('author_id')
    if not author_id:
        return "Must provide ID.", 400

    pubs = get_author_publications(author_id)
    return jsonify(pubs)
