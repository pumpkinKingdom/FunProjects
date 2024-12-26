from flask import Flask, request, jsonify
import requests
import os
from api import detect_clothes

app = Flask(__name__)

WEATHER_API_KEY = '11d56c37013e0a85958cf0c4fca769cc'

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    file.save('uploaded.jpg')  # Save the uploaded image

    # Call local function to detect clothing using the external API
    detected_clothes = detect_clothes('uploaded.jpg')

    # Fetch weather
    weather = getWeather()
    return jsonify({'recommendations': f'{detected_clothes} recommended for {weather}'})


def getWeather():
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q=London&appid={WEATHER_API_KEY}')
    if response.status_code == 200:
        weather_data = response.json()
        condition = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp'] - 273.15
        return f'{condition}, {round(temp, 1)}C'
    else:
        return 'Weather data unavailable'

if __name__ == '__main__':
    app.run(debug=True)

