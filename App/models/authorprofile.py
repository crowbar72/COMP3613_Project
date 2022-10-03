from App.database import db

class AuthorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    qualifications = db.Column(db.String(120), nullable=False)
    # publications = db.relationship("Publication")

    def __init__(self, name, dob, qualifications):
        self.name = name
        self.dob = dob
        self.qualifications = qualifications

    def toJSON(self):
        return{
            'id': id,
            'name': name,
            'dob': dob,
            'qualifications': qualifications
        }

