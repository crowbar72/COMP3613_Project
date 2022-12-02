from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required

from App.controllers import (
    create_author,
    check_author_exists,
    get_author,
    get_all_authors,
    get_all_authors_json,
    get_author_by_name,
    get_author_publications,
    get_author_publication_tree
)

author_views = Blueprint('author_views', __name__, template_folder='../templates')

@author_views.route('/author', methods=["POST"])
@jwt_required()
def create_author_route():
    data = request.get_json()
    # return jsonify(data)
    try:
        new_author = create_author(data['name'], data['dob'], data['qualifications'])
    except Exception as e:
        return f'Could not create due to exception: {e.__class__}', 400 
    return new_author.toJSON(), 201

@author_views.route('/author', methods=["GET"])
def get_author_route():
    authors = get_all_authors_json()
    return jsonify(authors)

@author_views.route('/api/pubtree', methods=['GET'])
def get_pub_tree():
    args = request.args
    author_id = args.get('author_id')
    if not author_id:
        return "Must provide ID.", 400
    treeList = []
    treeList = get_author_publication_tree(author_id, treeList)
    authorList = []
    for id in treeList:
        author = get_author(id)
        authorList.append(author.toJSON())
    return jsonify(authorList)