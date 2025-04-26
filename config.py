# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:RkktkRGZwdXAwXkEwtecHgYSdJEKGjFj"
        "@yamabiko.proxy.rlwy.net:36229/railway"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STRIPE_PUBLIC_KEY = 'pk_test_51RE7BEPFfDXYRYYJDO3ubsoT4BwW3V6GSVutYTRJ3b3pkcrK89wM7EYkPlJJSKsqw57R5rYVykXCUuUEfrK6uSCl000lUoBaAb'
    STRIPE_SECRET_KEY = 'sk_test_51RE7BEPFfDXYRYYJUVbFQB9d66jDTydSG6MO5vTOJf5SNIvy6x605XiGuH1GFjo2QQwS6pKba7x34NYbgmu3WAen00rRSOq7aW'
    ORS_API_KEY = '5b3ce3597851110001cf6248c3ea0212d9804a41b5fb786e5d14601b'
    ENDPOINT_SECRET = 'whsec_6QktntzOs64AXj1at5TimvFABga4siMf'

    # Email settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'nicosik04@gmail.com'
    MAIL_PASSWORD = 'wqok rxvx uwxa jvth'
    MAIL_DEFAULT_SENDER = ('Etaxi' , 'nicosik04@gmail.com')
    OPERATOR_EMAIL = 'goncharuk25250@gmail.com'  # постійна адреса оператора
