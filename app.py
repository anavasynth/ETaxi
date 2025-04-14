from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

ORS_API_KEY = '5b3ce3597851110001cf6248c3ea0212d9804a41b5fb786e5d14601b'

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

if __name__ == '__main__':
    app.run()
