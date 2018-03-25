import sys

from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project import db
from project.models import Schedule

from flask import current_app as app

schedule = Blueprint('schedule', __name__)

@schedule.route('/', methods=['GET'])
def index():
    return "Attendance schedule Service", 200

@schedule.route('/schedules', methods=['GET'])
def list_schedules():
    schedules = [table.to_dict() for table in Schedule.query.all()]
    response = {
        'status': 'success',
        'schedules': schedules
    }
    return jsonify(response), 200

    