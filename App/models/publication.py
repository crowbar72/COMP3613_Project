from App.database import db

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    authors = db.relationship("Author")

    def __init__(self, title, author):
        self.title = title
        self.author = author
    
    def toJSON(self):
        return{
            "title": self.title
        }