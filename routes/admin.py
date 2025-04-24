# routes/admin.py
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models import Ride, Transfer, Driver, db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/adminpanel')
def adminpanel():
    rides = Ride.query.all()
    transfers = Transfer.query.all()
    drivers = Driver.query.all()
    return render_template('adminpanel.html', rides=rides, transfers=transfers, drivers=drivers)

@admin_bp.route('/add_driver', methods=['POST'])
def add_driver():
    data = request.form
    driver = Driver(
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        driver_car=data['driver_car'],
        car_class=data['car_class']
    )
    db.session.add(driver)
    db.session.commit()
    return redirect(url_for('admin.adminpanel'))

@admin_bp.route('/delete_driver/<int:driver_id>', methods=['POST'])
def delete_driver(driver_id):
    driver = Driver.query.get(driver_id)
    if driver:
        db.session.delete(driver)
        db.session.commit()
    return redirect(url_for('admin.adminpanel'))

@admin_bp.route('/update_driver/<int:driver_id>', methods=['POST'])
def update_driver(driver_id):
    driver = Driver.query.get(driver_id)
    if driver:
        driver.first_name = request.form['first_name']
        driver.last_name = request.form['last_name']
        driver.phone = request.form['phone']
        driver.driver_car = request.form['driver_car']
        driver.car_class = request.form['car_class']
        db.session.commit()
    return redirect(url_for('admin.adminpanel'))


@admin_bp.route('/assign-driver' , methods = ['POST'])
def assign_driver():
    data = request.get_json()
    driver_id = data.get('driver_id')
    ride_id = data.get('ride_id')
    transfer_id = data.get('transfer_id')

    # Отримуємо водія
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({'status': 'error' , 'message': 'Driver not found'}) , 404

    driver_full_name = f"{driver.first_name} {driver.last_name}"
    print(driver_full_name)

    if ride_id:
        # Оновлюємо Ride
        ride = Ride.query.get(ride_id)
        if ride:
            ride.driver = driver_full_name
            db.session.commit()
            return jsonify({'status': 'success' , 'ride_id': ride_id , 'driver': driver_full_name})

    if transfer_id:
        # Оновлюємо Transfer
        transfer = Transfer.query.get(transfer_id)
        if transfer:
            transfer.driver = driver_full_name
            db.session.commit()
            return jsonify({'status': 'success' , 'transfer_id': transfer_id , 'driver': driver_full_name})

    return jsonify({'status': 'error' , 'message': 'Ride or Transfer not found'}) , 404
