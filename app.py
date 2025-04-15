from flask import Flask, render_template, request, jsonify
import requests
import hashlib
import time
import hmac
import stripe
app = Flask(__name__)

ORS_API_KEY = '5b3ce3597851110001cf6248c3ea0212d9804a41b5fb786e5d14601b'

SECRET_KEY = "flk3409refn54t54t*FNJRET"
MERCHANT_ACCOUNT = "test_merch_n1"
DOMAIN_NAME = "localhost"

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51RE7BEPFfDXYRYYJDO3ubsoT4BwW3V6GSVutYTRJ3b3pkcrK89wM7EYkPlJJSKsqw57R5rYVykXCUuUEfrK6uSCl000lUoBaAb'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51RE7BEPFfDXYRYYJUVbFQB9d66jDTydSG6MO5vTOJf5SNIvy6x605XiGuH1GFjo2QQwS6pKba7x34NYbgmu3WAen00rRSOq7aW'

stripe.api_key = app.config['STRIPE_SECRET_KEY']

class WayForPayHelper:
    def __init__(self, account, domain, key):
        self.account = account
        self.domain = domain
        self.key = key

    def get_signature(self, data):
        signature_text = (
            f"{self.account};"
            f"{self.domain};"
            f"{data['orderReference']};"
            f"{data['orderDate']};"
            f"{data['amount']};"
            f"{data['currency']};"
            f"{';'.join(data['productName'])};"
            f"{';'.join(str(c) for c in data['productCount'])};"
            f"{';'.join(str(p) for p in data['productPrice'])}"
        )
        return hmac.new(self.key.encode("utf-8"), signature_text.encode("utf-8"), hashlib.md5).hexdigest()

helper = WayForPayHelper(MERCHANT_ACCOUNT, DOMAIN_NAME, SECRET_KEY)

@app.route('/get-order-data' , methods = ['POST'])
def get_order_data():
    payload = request.json
    amount = payload.get('amount' , 100.0)
    client_email = payload.get('email' , 'client@example.com')
    client_phone = payload.get('phone' , '+380991234567')

    now = int(time.time())
    order_data = {
        "merchantAccount": MERCHANT_ACCOUNT ,
        "merchantDomainName": DOMAIN_NAME ,
        "orderReference": f"ORDER-{now}" ,
        "orderDate": now ,
        "amount": float(amount) ,
        "currency": "UAH" ,
        "productName": ["Послуга перевезення"] ,
        "productCount": [1] ,
        "productPrice": [float(amount)] ,
        "clientEmail": client_email ,
        "clientPhone": client_phone ,
        "language": "UA"
    }

    order_data["merchantSignature"] = helper.get_signature(order_data)
    return jsonify(order_data)

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/payment')
def payment():
    return "<h1>Оплата</h1><p>Тут буде сторінка оплати.</p>"

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        # Визначаємо хост
        if 'localhost' in request.host or '127.0.0.1' in request.host:
            base_url = 'http://localhost:5000'
        else:
            base_url = 'https://sockswebapp.onrender.com'

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'pln',
                    'product_data': {
                        'name': 'Оплата за поїздку',
                    },
                    'unit_amount': 500,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'{base_url}/success',
            cancel_url=f'{base_url}/cancel',
        )
        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

if __name__ == '__main__':
    app.run()
