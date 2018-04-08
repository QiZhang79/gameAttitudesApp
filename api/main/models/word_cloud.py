from db import db

class WordCloudModel(db.Document):
    keyword = db.StringField(required=True)
    related_keywords = db.StringField(required=True)
    datetime = db.StringField(required=True)

    def __init__(self, keyword, related_keywords, datetime, *args, **kwargs):
        super(db.Document, self).__init__()
        self.keyword = keyword
        self.related_keywords = related_keywords
        self.datetime = datetime

    def json(self):
        return {'keyword': self.keyword, 'related_keywords': self.related_keywords, 'datetime': self.datetime}

    @classmethod
    def find_by_keyword(cls, keyword):
        return cls.objects(keyword=keyword)

    @classmethod
    def aggregate_related_keywords(cls, related_keywords_list):
        pass


    def save_to_db(self):
        self.save()
