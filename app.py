from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
import random

app = Flask(__name__)

chat_messages = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/earthquakes')
def earthquakes():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    try:
        response = requests.get(url).json()
        latest_quakes = response['features'][:5]
    except:
        latest_quakes = []
    return render_template('earthquakes.html', quakes=latest_quakes)

@app.route('/wildfires', methods=['GET', 'POST'])
def wildfires():
    lat, lng = None, None
    if request.method == 'POST':
        lat = request.form.get('lat')
        lng = request.form.get('lng')
    return render_template('wildfires.html', lat=lat, lng=lng)

@app.route('/storms')
def storms():
    return render_template('storms.html')

@app.route('/analyze-sky', methods=['POST'])
def analyze_sky():
    density = random.randint(10, 100)
    status = "DANGER" if density > 80 else "CLEAR"
    return jsonify({"status": status, "density": density})

@app.route('/floods')
def floods():
    return render_template('floods.html')

@app.route('/extreme-heat')
def extreme_heat():
    return render_template('extreme_heat.html')

@app.route('/kit')
def kit():
    return render_template('kit.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/api/chat', methods=['GET', 'POST'])
def api_chat():
    if request.method == 'POST':
        data = request.json
        new_msg = {
            "user": data.get("user", "Anonymous"),
            "text": data.get("text", ""),
            "time": datetime.now().strftime("%H:%M")
        }
        chat_messages.append(new_msg)
        if len(chat_messages) > 50:
            chat_messages.pop(0)
        return jsonify({"status": "success"})
    return jsonify(chat_messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)