from flask import Blueprint, request, jsonify, current_app
import requests
from models import db, Ride

rides_bp = Blueprint('rides', __name__)

@rides_bp.route('/route' , methods = ['POST'])
def get_route():
    data = request.json
    coords = data['coordinates']

    # Отримуємо API ключ із конфігурації Flask
    ors_api_key = current_app.config['ORS_API_KEY']

    url = 'https://api.openrouteservice.org/v2/directions/driving-car/geojson'
    headers = {
        'Authorization': ors_api_key ,
        'Content-Type': 'application/json'
    }
    body = {
        "coordinates": coords
    }

    response = requests.post(url , json = body , headers = headers)
    return jsonify(response.json())


@rides_bp.route('/create-route-order' , methods = ['POST'])
def create_route_order():
    data = request.json
    print("data create:" , data)

    first_name = data.get('firstName')
    email = data.get('email')
    phone = data.get('phone')
    price = data.get('price')
    full_price = float(price) * 100 / 30
    car_class = data.get('carClass')

    start_address = data.get('startAddress')
    end_address = data.get('endAddress')

    payment_type = data.get('paymentType')  # full або partial
    ride_time_option = data.get('rideTimeOption')  # now або later
    scheduled_time = data.get('scheduledTime')  # дата-час або None

    # Формуємо поле для запису часу поїздки
    if ride_time_option == 'now' or scheduled_time is None:
        ride_time = 'зараз'
    else:
        ride_time = scheduled_time
    # Формуємо поле для запису типу оплати
    if payment_type == 'partial':
        # Якщо тільки 30% оплатили, вказуємо в дужках всю суму
        payment_info = f"30% (full price: {full_price})"
    else:
        payment_info = "Full"

    new_ride = Ride(
        first_name = first_name ,
        phone = phone ,
        email = email ,
        price = price ,
        car_class = car_class ,
        start_address = start_address ,
        end_address = end_address ,
        payment_status = 'pending' ,
        ride_time = ride_time ,
        payment_info = payment_info
    )

    db.session.add(new_ride)
    try:
        db.session.commit()
        return jsonify({"status": "success" , "id": new_ride.id}) , 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error" , "message": str(e)}) , 500