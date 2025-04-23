from flask import Flask, render_template, request, jsonify
import requests
import stripe
from db_orders import db, Transfer, Ride
from datetime import datetime
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mysql+pymysql://root:MUDxSvIyvCTacrNdPWTVLyYySRAfhqEZ"
    "@ballast.proxy.rlwy.net:30674/railway"
)


'''
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mysql+pymysql://root:1234"
    "@localhost/taxi_service"
)
'''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

#stripe
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51RE7BEPFfDXYRYYJDO3ubsoT4BwW3V6GSVutYTRJ3b3pkcrK89wM7EYkPlJJSKsqw57R5rYVykXCUuUEfrK6uSCl000lUoBaAb'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51RE7BEPFfDXYRYYJUVbFQB9d66jDTydSG6MO5vTOJf5SNIvy6x605XiGuH1GFjo2QQwS6pKba7x34NYbgmu3WAen00rRSOq7aW'

stripe.api_key = app.config['STRIPE_SECRET_KEY']

#maps
ORS_API_KEY = '5b3ce3597851110001cf6248c3ea0212d9804a41b5fb786e5d14601b'

# Файл для логів
LOG_FILE = 'stripe_webhook.log'

def log_to_file(message):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mainpage')
def mainpage():
    return render_template('mainpage.html')

@app.route('/transfers')
def transfers():
    return render_template('transfers.html')

@app.route('/route_details')
def route_details():
    return render_template('route_details.html')

@app.route('/route' , methods = ['POST'])
def get_route():
    data = request.json
    coords = data['coordinates']

    url = 'https://api.openrouteservice.org/v2/directions/driving-car/geojson'
    headers = {
        'Authorization': ORS_API_KEY ,
        'Content-Type': 'application/json'
    }
    body = {
        "coordinates": coords
    }

    response = requests.post(url , json = body , headers = headers)
    return jsonify(response.json())

# Встанови свій webhook secret з Stripe dashboard
endpoint_secret = 'whsec_6QktntzOs64AXj1at5TimvFABga4siMf'

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('stripe-signature')

    log_to_file("Webhook received")
    print("webhook received")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        log_to_file(f"Invalid payload: {e}")
        print(f"Invalid payload: {e}")
        return jsonify(success=False), 400
    except stripe.error.SignatureVerificationError as e:
        log_to_file(f"Signature error: {e}")
        print(f"Signature error: {e}")
        return jsonify(success=False), 400

    log_to_file(f"Event type: {event['type']}")
    print(f"Event type: {event['type']}")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata', {})
        payment_id = session['id']

        if 'order_id' in metadata:
            order_id = metadata['order_id']
            log_to_file(f"Checkout completed (Ride). Order ID: {order_id}, Payment ID: {payment_id}")
            print(f"Checkout completed (Ride). Order ID: {order_id}, Payment ID: {payment_id}")

            ride = Ride.query.filter_by(id=order_id).first()
            if ride:
                ride.payment_status = 'completed'
                ride.payment_id = payment_id
                db.session.commit()
                log_to_file(f"Ride #{order_id} updated in DB.")
                print(f"Ride #{order_id} updated in DB.")

        elif 'transfer_id' in metadata:
            transfer_id = metadata['transfer_id']
            log_to_file(f"Checkout completed (Transfer). Transfer ID: {transfer_id}, Payment ID: {payment_id}")
            print(f"Checkout completed (Transfer). Transfer ID: {transfer_id}, Payment ID: {payment_id}")

            transfer = Transfer.query.filter_by(id=transfer_id).first()
            if transfer:
                transfer.payment_status = 'completed'
                transfer.payment_id = payment_id
                db.session.commit()
                log_to_file(f"Transfer #{transfer_id} updated in DB.")
                print(f"Transfer #{transfer_id} updated in DB.")

    return jsonify(success=True), 200


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.get_json()
        print(data)
        price = data.get('price', 0)
        amount = int(float(price) * 100)

        # Визначаємо хост
        if 'localhost' in request.host or '127.0.0.1' in request.host:
            base_url = 'http://localhost:5000'
        else:
            base_url = 'https://sockswebapp.onrender.com'

        # Перевірка, що це: трансфер чи поїздка
        order_id = data.get('order_id')
        transfer_id = data.get('transfer_id')
        session_metadata = {}
        product_name = ''

        if order_id:
            session_metadata['order_id'] = str(order_id)
            product_name = 'Оплата за поїздку'
        elif transfer_id:
            session_metadata['transfer_id'] = str(transfer_id)
            product_name = 'Оплата за трансфер'
        else:
            return jsonify(error="order_id або transfer_id обов’язкові"), 400

        # Створюємо Stripe-сесію
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'pln',
                    'product_data': {'name': product_name},
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            metadata=session_metadata,
            mode='payment',
            success_url=f'{base_url}/success',
            cancel_url=f'{base_url}/cancel',
        )

        payment_id = session.id
        print("payment_id:", payment_id)

        # Зберігаємо session.id в базі
        if order_id:
            ride = Ride.query.filter_by(id=order_id).first()
            if ride:
                ride.payment_id = payment_id
                db.session.commit()
        elif transfer_id:
            transfer = Transfer.query.filter_by(id=transfer_id).first()
            if transfer:
                transfer.payment_id = payment_id
                db.session.commit()

        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.route('/create-transfer-order', methods=['POST'])
def create_transfer_order():
    data = request.json
    email = data.get('email')
    last_name = data.get('lastName')
    first_name = data.get('firstName')
    seats = data.get('seats')
    price = data.get('price')
    transfer = data.get('transfer')

    if isinstance(price, str) and 'PLN' in price:
        price = price.replace('PLN', '').strip()

    new_transfer = Transfer(
        email=email,
        last_name=last_name,
        first_name=first_name,
        seats=seats,
        price=price,
        transfer=transfer,
        payment_status='pending'  # можна додати статус
    )

    db.session.add(new_transfer)
    try:
        db.session.commit()
        return jsonify({"status": "success", "id": new_transfer.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/create-route-order', methods=['POST'])
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

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

@app.route('/adminpanel')
def adminpanel():
    rides = Ride.query.all()  # Отримати всі записи з таблиці Ride
    transfers = Transfer.query.all()  # Отримати всі записи з таблиці Ride
    return render_template('adminpanel.html', rides=rides, transfers=transfers)

if __name__ == '__main__':
    app.run()
