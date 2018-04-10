import datetime
import sys

from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project import db
from project.models import Schedule, Lecture

from flask import current_app as app

schedule = Blueprint('schedule', __name__)

@schedule.route('/', methods=['GET'])
def index():
    return "Attendance schedule Service", 200

@schedule.route('/schedules', methods=['GET'])
def list_schedules():
    lectures = [table.to_dict() for table in Lecture.query.all()]
    response = {
        'status': 'success',
        'schedules': lectures
    }
    return jsonify(response), 200

@schedule.route('/schedules/<room>', methods=['GET'])
def get_schedule(room):
    schedules = [lecture.to_dict() for lecture in Lecture.query.filter_by(room=room).all()]
    response = {
        'room': room,
        'schedule': schedules
    }
    return jsonify(response), 200

@schedule.route('/test', methods=['GET'])
def test_date_string():
    now = datetime.datetime.now() + datetime.timedelta(hours=1) #Hardcoding for Daylight savings for the moment
    start_time = now + datetime.timedelta(seconds=10)
    end_time = start_time + datetime.timedelta(seconds=30)
    lecture = {
        'id': 0,
        'lecturer': 'Dr. Test Testington',
        'subject': 'TEST LECTURE',
        'room': 'LB08',
        'start_time': start_time.strftime('%a, %d %b %Y %H:%M:%S'),
        'end_time': end_time.strftime('%a, %d %b %Y %H:%M:%S')
    }
    response = {
        'status': 'success',
        'schedule': [lecture]
    }
    return jsonify(response), 200


    