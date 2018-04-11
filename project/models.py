import datetime

from project import db


class Lecture(db.Model):
    __tablename__ = "lectures"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    room = db.Column(db.String(128), nullable=False)
    subject = db.Column(db.String(128), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True), nullable=False)
    end_time = db.Column(db.DateTime(timezone=True), nullable=False)
    lecturer = db.Column(db.String(128))
    students = db.relationship('AttendanceRecord', backref='lecture', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'room': self.room,
            'subject': self.subject,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'lecturer': self.lecturer,
            'status': self.status()
        }

    def from_dict(self, data):
        for field in ['room', 'subject', 'start_time', 'end_time', 'lecturer']:
            if field in data:
                setattr(self, field, data[field])

    def status(self):
        # start = datetime.datetime.strptime(self.start_time, '%a, %d %b %Y %H:%M:%S %Z')
        # end = datetime.datetime.strptime(self.end_time, '%a, %d %b %Y %H:%M:%S %Z')
        start = self.start_time
        end = self.end_time
        now = datetime.datetime.now(start.tzinfo)

        if now < start:
            return 'SCHEDULED'
        elif start <= now < end:
            return 'IN PROGRESS'
        else:
            return 'FINISHED'
    
class AttendanceRecord(db.Model):
    __tablename__ = "attendance_records"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    student_number = db.Column(db.String(128), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'student_number': self.student_number,
            'lecture_id': self.lecture_id
        }
