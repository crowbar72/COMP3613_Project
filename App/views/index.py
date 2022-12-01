from flask import Blueprint, redirect, render_template, request, send_from_directory

from App.controllers import (
    PubtreeForm,
    get_author_by_name,
    getpublicationtree
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/signuppage', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@index_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@index_views.route('/newpub', methods=['GET'])
def new_publication_page():
    return render_template('newpub.html')

@index_views.route('/results', methods=['GET'])
def search_results_page():
    return render_template('results.html')

@index_views.route('/pubtree', methods=['GET'])
def publication_tree_page():
    form = PubtreeForm()
    return render_template('pubtree.html', form=form)

@index_views.route('/pubtree', methods=['POST'])
def publication_tree_search():
    form = PubtreeForm()
    if form.validate_on_submit():
        data = request.form
        user = get_author_by_name(data["AuthorName"])
        if user is not None:
            tree = getpublicationtree(user.id)
            return render_template('pubtree.html', form=form, tree=tree)
    return render_template('pubtree.html', form=form)