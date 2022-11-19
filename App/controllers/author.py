from App.models import Author
from App.database import db

def create_author(name, dob, qualifications):
    new_author = Author(name=name, dob=dob, qualifications=qualifications)
    db.session.add(new_author)
    db.session.commit()
    return new_author

def check_author_exists(name):
    author = Author.query.filter_by(name=name)
    if not author:
        new_author = create_author(name=name, dob=None, qualifications=None)
        return new_author
    return author

def get_author(id):
    return Author.query.get(id)

def get_all_authors():
    return Author.query.all()

def get_all_authors_json():
    authors = Author.query.all()
    if not Author:
        return []
    authors = [author.toJSON() for author in authors]
    return authors

def get_author_by_name(name):
    print(name)
    author = Author.query.filter_by(name=name).first()
    if not author:
        return []
    return author

def get_author_publications(id):
    author = get_author(id)
    if not author:
        return []
    return author.get_publications()

def getpublicationtree(id):
    author = get_author(id)
    if not author:
        return []
    return author.get_publications()
    