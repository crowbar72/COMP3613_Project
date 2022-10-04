from App.database import db
# from .author import *
from .authorprofile import *

AuthorPublication = db.Table(
    "authorpublication",
    db.Column("authorprofile_id", db.ForeignKey("authorprofile.id"), primary_key=True),
    db.Column("publication_id", db.ForeignKey("publication.id"), primary_key=True),
)

class Publication(db.Model):
    __tablename__ = "publication"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    # authors = db.relationship("Author")
    authors = db.relationship(AuthorProfile, secondary=AuthorTable, backref=db.backref('publication'))

    def __init__(self, title, author):
        self.title = title
    
    def toJSON(self):
        return{
            "title": self.title
        }

