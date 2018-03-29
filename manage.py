import json
import os

from flask_script import Manager

from project import create_app, db
from project.models import Schedule, Lecture

app = create_app()
manager = Manager(app)

@manager.command
def recreate_db():
    """Recreate a new empty database"""
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def seed_db():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_directory, 'seeds.json')

    with open(filepath, 'r') as f:
        data = json.load(f)

    for entry in data['lectures']:
        lecture = Lecture()
        lecture.from_dict(entry)
        db.session.add(lecture)
        db.session.commit()

if __name__ == '__main__':
    manager.run()
    