from flask_restful import Resource, reqparse
from main.models.word_cloud import WordCloudModel
import json

class WordCloud(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('related_keywords',
        type=str,
        required=True,
    )
    parser.add_argument('datetime',
        type=str,
        required=True,
    )

    def get(self, keyword):
        related_keywords = WordCloudModel.find_by_keyword(keyword)
        results = []
        for x in related_keywords:
            results.append({'keyword': x.keyword, 'related_keywords': x.related_keywords, 'datetime': x.datetime})
        return {'related_keywords': results}, 201


    def post(self, keyword):
        data = self.parser.parse_args()
        word_cloud = WordCloudModel(keyword, data['related_keywords'], data['datetime'])
        try:
            word_cloud.save_to_db()
        except Exception as e:
            return {"message": str(e)}, 500

        return word_cloud.json(), 201


class WordCloudSum(Resource):
    def get(self, keyword):
        res_dict = {}
        res_li = []
        related_keywords = WordCloudModel.find_by_keyword(keyword)
        if len(related_keywords) > 50:
            related_keywords = related_keywords[:50]
        for x in related_keywords:
            x.related_keywords = x.related_keywords.replace('"', '*')
            x.related_keywords = x.related_keywords.replace("'", '"')
            x.related_keywords = x.related_keywords.replace("*", "'")
            try:
                x_dict = json.loads(x.related_keywords)
            except:
                x_dict = {}

            for key, val in x_dict.items():
                if key in res_dict:
                    try:
                        res_dict[key] += val
                    except:
                        res_dict[key] += 0
                else:
                    res_dict[key] = val

        for key, val in res_dict.items():
            res_li.append((key, val))

        res_li = sorted(res_li, key=lambda x: x[1], reverse=True)

        if len(res_li) > 20:
            return res_li[:20]

        return {'related_keywords_sum': res_li}, 201
