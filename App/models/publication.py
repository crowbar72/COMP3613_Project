from App.database import db
from .author import *
from .author_publication import *

class Publication(db.Model):
    __tablename__ = "publication"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, unique=False)
    authorId = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)
    coauthors = db.relationship("Author", secondary=CoAuthorPublication)

    def __init__(self, title, authorId, coauthors):
        self.title = title
        self.authorId = authorId
        if coauthors:
            self.coauthors.extend(coauthors)
    
    def toJSON(self):
        return{
            "id": self.id,
            "title": self.title, 
            "author": self.authorId,
            "coauthors": [coauthor.toJSON() for coauthor in self.coauthors]
        }
