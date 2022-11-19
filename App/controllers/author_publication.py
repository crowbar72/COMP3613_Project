from App.models import CoAuthorPublication
from App.database import db

def get_all_items_json():
    rows = CoAuthorPublication.query.all()
    if not rows:
        return []
    rows = [row.toJSON() for row in rows]
    return rows 