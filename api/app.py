from flask import Flask, render_template
from flask_restful import Api

from main.resources.analysis import Analysis, AnalysisList, AnalysisPoint, AnalysisCount
from main.resources.keyword import Keyword
from main.resources.word_cloud import WordCloud, WordCloudSum

import requests
import json

# app instance
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': 'db',
    'db': 'twitter-analysis',
    'port': 27017
}

# Api instance
api = Api(app)

# Resource URL binding
api.add_resource(Analysis, '/analysis/<string:keyword>')
api.add_resource(AnalysisList, '/analysis')
api.add_resource(AnalysisPoint, '/analysis/<string:keyword>/point')
api.add_resource(AnalysisCount, '/analysis/<string:keyword>/count')
api.add_resource(Keyword, '/keyword')
api.add_resource(WordCloud, '/wordcloud/<string:keyword>')
api.add_resource(WordCloudSum, '/wordcloud/<string:keyword>/sum')

# Homepage
@app.route('/', methods=['GET'])
def index():
    analysis_point = AnalysisPoint()
    analysis_count = AnalysisCount()
    wordcloud_sum = WordCloudSum()

    try:
        analysis_point_nintendo = analysis_point.get('nintendo')[0]['point']
    except Exception as e:
        analysis_point_nintendo = str(e)
    try:
        analysis_point_playstation = analysis_point.get('playstation')[0]['point']
    except Exception as e:
        analysis_point_playstation = str(e)
    try:
        analysis_point_xbox = analysis_point.get('xbox')[0]['point']
    except Exception as e:
        analysis_point_xbox = str(e)

    try:
        analysis_count_nintendo = analysis_count.get('nintendo')[0]['tweet_count']
    except Exception as e:
        analysis_count_nintendo = str(e)
    try:
        analysis_count_playstation = analysis_count.get('playstation')[0]['tweet_count']
    except Exception as e:
        analysis_count_playstation = str(e)
    try:
        analysis_count_xbox = analysis_count.get('xbox')[0]['tweet_count']
    except Exception as e:
        analysis_count_xbox = str(e)

    try:
        wordcloud_sum_nintendo = wordcloud_sum.get('nintendo')
    except Exception as e:
        wordcloud_sum_nintendo = str(e)
    try:
        wordcloud_sum_playstation = wordcloud_sum.get('playstation')
    except Exception as e:
        wordcloud_sum_playstation = str(e)
    try:
        wordcloud_sum_xbox = wordcloud_sum.get('xbox')
    except Exception as e:
        wordcloud_sum_xbox = str(e)

    return render_template("index.html", **locals())


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
