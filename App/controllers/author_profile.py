from App.models import AuthorProfile
from App.database import db

def create_author(name, dob, qualifications):
    new_author = AuthorProfile(name=name, dob=dob, qualifications=qualifications)
    db.session.add(new_author)
    db.session.commit()
    return new_author

def get_author(id):
    return AuthorProfile.query.get(id)

def get_all_authors():
    return AuthorProfile.query.all()

def get_all_authors_json():
    authors = AuthorProfile.query.all()
    if not AuthorProfile:
        return []
    authors = [author.toJSON() for author in authors]
    return authors