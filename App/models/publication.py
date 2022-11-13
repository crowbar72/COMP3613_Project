from App.database import db
from .author import *
from .author_publication import *

class Publication(db.Model):
    __tablename__ = "publication"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, unique=True)
    authorId = db.Column(db.Integer, ForeignKey("parent_table.id"). nullable=False)
    coauthors = db.relationship("Author", secondary=CoAuthorPublication)

    def __init__(self, title, author, coauthors):
        self.title = title
        self.author.extend(author)
        if coauthors:
            self.coauthors.extend(coauthors)
    
    def toJSON(self):
        return{
            "id": self.id,
            "title": self.title, 
            "author": Author.query.get(id).toJSON(),
            "coauthors": [coauthor.toJSON() for coauthor in self.coauthors]
        }
