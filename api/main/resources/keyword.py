from flask_restful import Resource, reqparse
from main.models.keyword import KeywordModel

class Keyword(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('keyword',
        type=str,
        required=True,
    )


    def get(self):
        keyword = KeywordModel.get_keyword()['keyword']
        return {'keyword': keyword}, 201


    def post(self):
        data = self.parser.parse_args()
        keyword = KeywordModel(data['keyword'])

        try:
            keyword.save_to_db()
        except Exception as e:
            return {"message": str(e)}, 500

        return keyword.json(), 201
