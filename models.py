from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transfer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20) , nullable = False)
    seats = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    transfer_date = db.Column(db.DateTime , nullable = False)  # <--- НОВЕ ПОЛЕ (дата поїздки)
    payment_type = db.Column(db.String(255) , nullable = False)  # <--- НОВЕ ПОЛЕ (тип оплати)


    transfer = db.Column(db.String(255), nullable=False)
    payment_status = db.Column(db.String(50), default='pending')
    payment_id = db.Column(db.String(255) , nullable = True)  # Поле для збереження ID оплати
    driver = db.Column(db.String(255), nullable=True)  #


    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    car_class = db.Column(db.String(255), nullable=True) # Клас авто
    price = db.Column(db.Numeric(10, 2), nullable=False)

    ride_time = db.Column(db.String(255) , nullable = True)
    payment_info = db.Column(db.String(255) , nullable = True)

    start_address = db.Column(db.String(255), nullable=False)
    end_address = db.Column(db.String(255), nullable=False)

    payment_status = db.Column(db.String(50), default='pending')
    payment_id = db.Column(db.String(255), nullable=True)  # Поле для збереження ID оплати
    driver = db.Column(db.String(255), nullable=True)  # Для вибору водія
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    driver_car =db.Column(db.String(255), nullable=False)
    car_class = db.Column(db.String(255), nullable=False)
    car_number = db.Column(db.String(255), nullable=False)
