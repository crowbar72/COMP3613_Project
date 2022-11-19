from App.database import db


# AuthorPublication = db.Table(
#     "authorpublication",
#     db.Column("author_id", db.ForeignKey("author.id"), primary_key=True),
#     db.Column("publication_id", db.ForeignKey("publication.id"), primary_key=True)
# )

CoAuthorPublication = db.Table(
    "coauthorpublication",
    db.Column("author_id", db.ForeignKey("author.id"), primary_key=True),
    db.Column("publication_id", db.ForeignKey("publication.id"), primary_key=True)
)