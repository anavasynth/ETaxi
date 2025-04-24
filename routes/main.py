# routes/main.py
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/mainpage')
def mainpage():
    return render_template('mainpage.html')

@main_bp.route('/route_details')
def route_details():
    return render_template('route_details.html')
