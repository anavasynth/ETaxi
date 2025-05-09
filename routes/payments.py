# routes/payments.py
from flask import Blueprint, request, jsonify, render_template
import stripe
from models import db, Ride, Transfer
from config import Config
from datetime import datetime
from helpers.email_utils import send_email

payments_bp = Blueprint('payments', __name__)

stripe.api_key = Config.STRIPE_SECRET_KEY

LOG_FILE = 'stripe_webhook.log'

def log_to_file(message):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")

@payments_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('stripe-signature')

    log_to_file("Webhook received")
    print("webhook received")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, Config.ENDPOINT_SECRET)
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

                # --- Після успішної оплати відправити листи ---
                subject = "Підтвердження замовлення"
                operator_subject = f"Нове замовлення #{ride.id}"

                # Підготувати дані для підставлення
                context = {
                    "customer_name": ride.first_name ,
                    "phone": ride.phone ,
                    "email": ride.email ,
                    "start_address": ride.start_address ,
                    "end_address": ride.end_address ,
                    "car_class": ride.car_class ,
                    "date_time": ride.ride_time ,
                    "price": ride.price ,
                    "payment_type": ride.payment_info ,
                    "type": "Ride"  # або "Трансфер"
                }

                # Зрендерити шаблони
                client_body = render_template('client_email.html' , **context)
                operator_body = render_template('operator_email.html' , **context)

                # Надіслати листи
                send_email(subject , [ride.email] , html_body = client_body)
                send_email(operator_subject , [Config.OPERATOR_EMAIL] , html_body = operator_body)

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

                # --- Після успішної оплати відправити листи ---
                subject = "Підтвердження замовлення"
                operator_subject = f"Нове замовлення #{transfer.id}"

                # Підготувати дані для підставлення
                context = {
                    "customer_name": transfer.first_name ,
                    "phone": transfer.phone ,
                    "email": transfer.email ,
                    "transfer": transfer.transfer ,
                    "seats": transfer.seats ,
                    "date_time": transfer.transfer_date ,
                    "price": transfer.price ,
                    "payment_type": transfer.payment_type ,
                    "type": "Transfer"  # або "Трансфер"
                }

                # Зрендерити шаблони
                client_body = render_template('client_email.html' , **context)
                operator_body = render_template('operator_email.html' , **context)

                # Надіслати листи
                send_email(subject , [transfer.email] , html_body = client_body)
                send_email(operator_subject , [Config.OPERATOR_EMAIL] , html_body = operator_body)

                log_to_file(f"Transfer #{transfer_id} updated in DB.")
                print(f"Transfer #{transfer_id} updated in DB.")

    return jsonify(success=True), 200

@payments_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.get_json()
        print(data)
        price = data.get('price', 0)
        amount = int(float(price) * 100)

        base_url = request.host_url.rstrip('/')

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

@payments_bp.route('/success')
def success():
    return render_template('success.html')

@payments_bp.route('/cancel')
def cancel():
    return render_template('cancel.html')