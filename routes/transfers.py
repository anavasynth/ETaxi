# routes/transfers.py
from flask import Blueprint, render_template, request, jsonify
from models import db, Transfer

transfers_bp = Blueprint('transfers', __name__)

@transfers_bp.route('/transfers')
def transfers():
    return render_template('transfers.html')

@transfers_bp.route('/transfer_auschwitz')
def transfer_auschwitz():
    return render_template('transfers/transfer_auschwitz.html')

@transfers_bp.route('/transfer_zator')
def transfer_zator():
    return render_template('transfers/transfer_zator.html')

@transfers_bp.route('/transfer_zakopane')
def transfer_zakopane():
    return render_template('transfers/transfer_zakopane.html')

@transfers_bp.route('/transfer_katowice_pyrzowice')
def transfer_katowice_pyrzowice():
    return render_template('transfers/transfer_katowice_pyrzowice.html')

@transfers_bp.route('/transfer_wieliczka')
def transfer_wieliczka():
    return render_template('transfers/transfer_wieliczka.html')

@transfers_bp.route('/transfer_teczyn')
def transfer_teczyn():
    return render_template('transfers/transfer_teczyn.html')

@transfers_bp.route('/transfer_john_paul')
def transfer_john_paul():
    return render_template('transfers/transfer_john_paul.html')

@transfers_bp.route('/transfer_city_transfer')
def transfer_city_transfer():
    return render_template('transfers/transfer_city_transfer.html')

@transfers_bp.route('/create-transfer-order', methods=['POST'])
def create_transfer_order():
    data = request.json
    first_name = data.get('firstName')
    email = data.get('email')
    phone = data.get('phone')
    seats = data.get('seats')
    price = data.get('price')
    transfer = data.get('transfer')

    if isinstance(price, str) and 'PLN' in price:
        price = price.replace('PLN', '').strip()

    new_transfer = Transfer(
        first_name=first_name,
        email = email,
        phone = phone,
        seats=seats,
        price=price,
        transfer=transfer,
        payment_status='pending'
    )

    db.session.add(new_transfer)
    try:
        db.session.commit()
        return jsonify({"status": "success", "id": new_transfer.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
