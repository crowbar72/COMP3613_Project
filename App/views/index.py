from flask import Blueprint, redirect, render_template, request, send_from_directory

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
def search_results_page():
    return render_template('pubtree.html')