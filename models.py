from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transfer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    seats = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    transfer = db.Column(db.String(255), nullable=False)
    payment_status = db.Column(db.String(50), default='pending')
    payment_id = db.Column(db.String(255) , nullable = True)  # Поле для збереження ID оплати
    driver = db.Column(db.String(255), nullable=True)  # Додайте це поле
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    car_class = db.Column(db.String(255), nullable=True) # Клас авто
    phone = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
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

    def to_dict(self):
        return {
            'id': self.id ,
            'first_name': self.first_name ,
            'last_name': self.last_name ,
            'phone': self.phone ,
            'driver_car': self.driver_car ,
            'car_class': self.car_class
        }
