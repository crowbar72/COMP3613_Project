from App.database import db
from datetime import *

class AuthorProfile(db.Model):
    __tablename__ = "authorprofile"
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String, nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    qualifications = db.Column(db.String(120), nullable=False)
    # publications = db.relationship("Author")

    def __init__(self, name, dob, qualifications):
        self.name = name
        self.dob = datetime.strptime(dob, "%d/%m/%Y")
        self.qualifications = qualifications

    def toJSON(self):
        return{
            'id': self.id,
            'name': self.name,
            'dob': self.dob,
            'qualifications': self.qualifications
        }

