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

@rides_bp.route('/create-route-order', methods=['POST'])
def create_route_order():
    data = request.json
    print("data create:", data)
    first_name = data.get('firstName')
    phone = data.get('phone')
    price = data.get('price')
    car_class = data.get('carClass')

    new_ride = Ride(
        first_name=first_name,
        phone=phone,
        price=price,
        car_class=car_class,
        payment_status='pending'
    )
    db.session.add(new_ride)
    try:
        db.session.commit()
        return jsonify({"status": "success", "id": new_ride.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500