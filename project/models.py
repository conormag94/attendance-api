from project import db

class Schedule(db.Model):
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Lecture(db.Model):
    __tablename__ = "lectures"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    room = db.Column(db.String(128), nullable=False)
    subject = db.Column(db.String(128), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True), nullable=False)
    end_time = db.Column(db.DateTime(timezone=True), nullable=False)
    lecturer = db.Column(db.String(128))

    def to_dict(self):
        return {
            'id': self.id,
            'room': self.room,
            'subject': self.subject,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'lecturer': self.lecturer
        }

    def from_dict(self, data):
        for field in ['room', 'subject', 'start_time', 'end_time', 'lecturer']:
            if field in data:
                setattr(self, field, data[field])
    
