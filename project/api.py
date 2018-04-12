import datetime
import sys

from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project import db
from project.models import Lecture, AttendanceRecord

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
    start_time = now + datetime.timedelta(seconds=15)
    end_time = start_time + datetime.timedelta(seconds=30)
    lecture = {
        'id': 1,
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

@schedule.route('/lectures/<id>', methods=['GET', 'POST'])
def get_lecture(id):
    lecture = Lecture.query.get(id)
    if not lecture:
        return jsonify({'status': 'fail', 'message': 'Lecture does not exist'}), 404
    
    if request.method == 'GET':
        students = [student.student_number for student in lecture.students]
        response = {
            'status': 'success',
            'lecture': lecture.to_dict(),
            'students': students
        }
        return jsonify(response), 200
    elif request.method == 'POST':
        params = request.get_json()
        student_numbers = params.get('student_numbers')
        for number in student_numbers:
            record = AttendanceRecord(student_number=number, lecture=lecture)
            db.session.add(record)
            db.session.commit()
        return jsonify({
            'status': 'success', 
            'message': 'Attendance for lecture {0} recorded'.format(lecture.id)
        }), 201
    