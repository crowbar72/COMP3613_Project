from App.models import CoAuthorPublication
from App.database import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class PubtreeForm(FlaskForm):
    authorName = StringField("AuthorName", validators=[InputRequired()])
    submit = SubmitField("PubtreeSubmit", render_kw={"class": "btn"})

def get_all_items_json():
    rows = CoAuthorPublication.query.all()
    if not rows:
        return []
    rows = [row.toJSON() for row in rows]
    return rows 