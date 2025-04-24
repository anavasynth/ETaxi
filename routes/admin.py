# routes/admin.py
from flask import Blueprint, render_template
from models import Ride, Transfer

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/adminpanel')
def adminpanel():
    rides = Ride.query.all()
    transfers = Transfer.query.all()
    return render_template('adminpanel.html', rides=rides, transfers=transfers)