from flask_restful import Resource, reqparse
from main.models.analysis import AnalysisModel


class Analysis(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('pos_cnt',
        type=int,
        required=True,
    )
    parser.add_argument('neg_cnt',
        type=int,
        required=True,
    )
    parser.add_argument('datetime',
        type=str,
        required=True,
    )

    def get(self, keyword):
        analysis = AnalysisModel.find_by_keyword(keyword)
        result = []
        for x in analysis:
            result.append({'keyword': x.keyword, 'pos_cnt': x.pos_cnt, 'neg_cnt': x.neg_cnt, 'datetime': x.datetime})
        return {'analysis': result}, 201


    def post(self, keyword):
        data = self.parser.parse_args()
        analysis = AnalysisModel(keyword, data['pos_cnt'], data['neg_cnt'], data['datetime'])

        try:
            analysis.save_to_db()
        except Exception as e:
            return {"message": str(e)}, 500

        return analysis.json(), 201


class AnalysisList(Resource):
    def get(self):
        keywords = AnalysisModel.get_all_keywords()
        return {'Analyzed keywords': keywords}


class AnalysisCount(Resource):
    def get(self, keyword):
        count = AnalysisModel.get_tweet_count(keyword)
        return {'tweet_count': count}, 201


class AnalysisPoint(Resource):

    def get(self, keyword):
        point = AnalysisModel.get_positive_ratio_by_keyword(keyword)
        return {'keyword': keyword, 'point': str(point*100)+'%'}, 201
