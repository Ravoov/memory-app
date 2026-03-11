from config import db


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    memory_score = db.Column(db.Integer, nullable=False)
    sleep_score = db.Column(db.Integer, nullable = False)
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "sleep_score": self.sleep_score,
            "memory_score": self.memory_score,
        }