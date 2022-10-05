from App.models import Author
from App.database import db

def create_author(name, dob, qualifications):
    new_author = Author(name=name, dob=dob, qualifications=qualifications)
    db.session.add(new_author)
    db.session.commit()
    return new_author

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
    authors = Author.query.filter_by(name=name)
    # if not authors:
    #     return []
    authors = [author for author in authors]
    print(authors)
    return authors
    