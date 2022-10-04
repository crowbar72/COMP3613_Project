from App.database import db


# class Author(db.Model):
#     author_id = db.Column(db.Integer, db.ForeignKey("authorprofile.id"), primary_key=True)
#     publication_id = db.Column(db.Integer, db.ForeignKey("publication.id"), primary_key=True)

#     def __init__(self, author_id, publication_id):
#         self.author_id = author_id
#         self.publication_id = publication_id

#     def toJSON(self):
#         return{
#             'author_id': author_id,
#             'publication_id': publication_id
#         }

