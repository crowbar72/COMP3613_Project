from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required

from App.controllers import (
    create_publication,
    get_publication,
    get_all_publications,
    get_all_publications_json,
    get_author_publications,
    get_author_by_name,
    check_author_exists
)

publication_views = Blueprint('publication_views', __name__, template_folder='../templates')

@publication_views.route('/publications', methods=["GET"])
def get_publications():
    args = request.args
    if not args:
        pubs = get_all_publications_json()
        return jsonify(pubs), 200
    author_id = args.get("author")
    query = args.get("query")
    pubs = []
    if author_id:
        pubs = get_author_publications(author_id)
    if query:
        query = query.lower()
        print(query)
        pubs = filter(lambda pub: query in pub['title'].lower(), pubs)
    return jsonify(list(pubs)), 200
        

@publication_views.route('/publications', methods=["POST"])
@jwt_required()
def post_publication():
    data = request.get_json()
    author_name = data['author']
    coauthor_names = data['coauthors']
    author = get_author_by_name(author_name)
    coauthors = [check_author_exists(name) for name in coauthor_names]
    
    # return jsonify(author_names)
    try:
        new_pub = create_publication(data['title'], author.id, coauthors)
    except Exception as e:
        return f'Could not create due to exception: {e.__class__}', 400
    return new_pub.toJSON(), 201