from flask_restful import Resource
from flask_restful import fields, marshal_with

from application.database import db
from application.models import Userdetails, Cards, Deck

output_fields = {
    "card_id" : fields.Integer,
    "language" : fields.String,
    "front" : fields.String,
    "back" : fields.String
}



class USERAPI(Resource):
    @marshal_with(output_fields)
    def get(self, language):
        cards = db.session.query(Cards).filter(Cards.language == language).all()

        if cards:
            return cards
        else:
            return None, 404
