from app import db
from . import PaginatedAPIMixin, User

class Tlahtolli(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(120), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    definition = db.Column(db.String(120))
    state = db.Column(db.String(10), db.CheckConstraint("state in ['known','tlahtolli','ignore']"))

    def to_dict(self):
        data = {
            'id':self.id,
            'word':self.word,
            'user_id':self.user_id,
            'definition':self.definition,
            'state':self.state
        }
        return data

    def from_dict(self, data):
        for field in ['word', 'user_id', 'definition', 'state']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return '<{} {}>'.format(self.word, User.query.filter_by(id=self.user_id).first().username)
