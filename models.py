from server import db

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    gender = db.Column(db.Integer)
    birth = db.Column(db.DateTime)
    note = db.Column(db.Text)
    deleted = db.Column(db.Boolean)
    
    def __init__(self, name, gender, birth, note, deleted = None):
        self.name = name
        self.gender = gender
        self.birth = birth
        self.note = note
        self.deleted = deleted

    def serialize(self):
        birth_formatted = self.birth.strftime("%Y-%m-%d") if self.birth else None
        return {
            "id":self.id,
            "name": self.name,
            "gender": self.gender,
            "birth": birth_formatted,
            "note": self.note,
            "deleted": self.deleted
        }