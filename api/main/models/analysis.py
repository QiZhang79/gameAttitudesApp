from db import db


class AnalysisModel(db.Document):
    keyword = db.StringField(required=True)
    pos_cnt = db.IntField(required=True)
    neg_cnt = db.IntField(required=True)
    datetime = db.StringField(required=True)

    def __init__(self, keyword, pos_cnt, neg_cnt, datetime, *args, **kwargs):
        super(db.Document, self).__init__()
        self.keyword = keyword
        self.pos_cnt = pos_cnt
        self.neg_cnt = neg_cnt
        self.datetime = datetime

    def json(self):
        return {'keyword': self.keyword, 'pos_cnt': self.pos_cnt, 'neg_cnt': self.neg_cnt, 'datetime': self.datetime}

    @classmethod
    def find_by_keyword(cls, keyword):
        return cls.objects(keyword=keyword)

    def save_to_db(self):
        self.save()

    @classmethod
    def get_all_keywords(cls):
        return cls.objects().distinct('keyword')

    @classmethod
    def get_tweet_count(cls, keyword):
        pos = cls.objects(keyword=keyword).sum('pos_cnt')
        neg = cls.objects(keyword=keyword).sum('neg_cnt')
        return pos + neg

    @classmethod
    def get_positive_ratio_by_keyword(cls, keyword):
        pos = cls.objects(keyword=keyword).sum('pos_cnt')
        neg = cls.objects(keyword=keyword).sum('neg_cnt')
        if neg == 0:
            return 1
        return 1.0*pos/(pos+neg)
