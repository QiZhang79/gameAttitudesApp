from db import db


class KeywordModel(db.Document):
    keyword = db.StringField(required=True)

    def __init__(self, keyword, *args, **kwargs):
        super(db.Document, self).__init__()
        self.keyword = keyword

    def json(self):
        return {'keyword': self.keyword}

    @classmethod
    def get_keyword(cls):
        return cls.objects().first()

    def save_to_db(self):
        KeywordModel.objects().delete()
        self.save()
