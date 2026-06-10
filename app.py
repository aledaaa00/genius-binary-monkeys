from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
import random

app = Flask(__name__)

chat_messages = []
sos_events = []
volunteers = []

def get_latest_alert():
    alerts = [
        "🚨 LATEST EVENT: Magnitude 6.2 Earthquake detected in the Pacific Ring of Fire.",
        "🔥 LATEST EVENT: High Wildfire Risk reported in western arid sectors. Wind vectors expanding.",
        "🌪️ LATEST EVENT: Severe atmospheric anomalies detected. Tornado warning in effect.",
        "☀️ LATEST EVENT: WBGT index reaching critical levels in equatorial sectors. Hydration advised."
    ]
    return random.choice(alerts)

@app.route('/')
def home():
    return render_template('index.html', ticker=get_latest_alert())

@app.route('/earthquakes')
def earthquakes():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    try:
        response = requests.get(url).json()
        latest_quakes = response['features'][:5]
    except:
        latest_quakes = []
    return render_template('earthquakes.html', quakes=latest_quakes, ticker=get_latest_alert())

@app.route('/wildfires', methods=['GET', 'POST'])
def wildfires():
    lat, lng = None, None
    if request.method == 'POST':
        lat = request.form.get('lat')
        lng = request.form.get('lng')
    return render_template('wildfires.html', lat=lat, lng=lng, ticker=get_latest_alert())

@app.route('/storms')
def storms():
    return render_template('storms.html', ticker=get_latest_alert())

@app.route('/analyze-sky', methods=['POST'])
def analyze_sky():
    density = random.randint(10, 100)
    status = "DANGER" if density > 80 else "CLEAR"
    return jsonify({"status": status, "density": density})

@app.route('/floods')
def floods():
    return render_template('floods.html', ticker=get_latest_alert())

@app.route('/extreme-heat')
def extreme_heat():
    temp = random.randint(35, 45)
    hum = random.randint(50, 90)
    danger = "CRITICAL - Lethal Wet-Bulb Temp" if (temp > 38 and hum > 60) else "MODERATE - Stay Hydrated"
    return render_template('extreme_heat.html', temp=temp, hum=hum, danger=danger, ticker=get_latest_alert())

@app.route('/kit')
def kit():
    return render_template('kit.html', ticker=get_latest_alert())

@app.route('/chat')
def chat():
    return render_template('chat.html', ticker=get_latest_alert())

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

@app.route('/api/sos', methods=['GET', 'POST'])
def api_sos():
    if request.method == 'POST':
        data = request.json
        new_event = {
            "type": data.get("type", "Unknown Event"),
            "desc": data.get("desc", ""),
            "lat": data.get("lat"),
            "lng": data.get("lng"),
            "time": datetime.now().strftime("%H:%M")
        }
        sos_events.append(new_event)
        return jsonify({"status": "success"})
    return jsonify(sos_events)

@app.route('/api/volunteers', methods=['GET', 'POST'])
def api_volunteers():
    if request.method == 'POST':
        data = request.json
        new_vol = {
            "name": data.get("name", "Volunteer"),
            "skills": data.get("skills", "General Support"),
            "lat": data.get("lat"),
            "lng": data.get("lng")
        }
        volunteers.append(new_vol)
        return jsonify({"status": "success"})
    return jsonify(volunteers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)