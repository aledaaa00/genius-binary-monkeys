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


@app.route('/triage')
def triage():
    return render_template('triage.html', ticker=get_latest_alert())


@app.route('/api/triage', methods=['POST'])
def api_triage():
    data = request.json
    injury = data.get("injury", "").lower()

    if "burn" in injury or "arsur" in injury or "foc" in injury:
        advice = [
            "1. STOP the burning process immediately.",
            "2. COOL the burn with cool (not cold) running water for at least 10 minutes.",
            "3. REMOVE jewelry or tight items near the burn before it swells.",
            "4. COVER the burn loosely with a sterile, non-adhesive bandage.",
            "⚠️ DO NOT apply ice, butter, or ointments to severe burns."
        ]
        severity = "HIGH RISK"
    elif "cut" in injury or "bleeding" in injury or "taietur" in injury or "sange" in injury:
        advice = [
            "1. APPLY DIRECT PRESSURE to the wound using a clean cloth or sterile dressing.",
            "2. ELEVATE the injured area above the heart if possible.",
            "3. KEEP PRESSURE for at least 10-15 minutes without peeking.",
            "4. IF BLEEDING SEEPS THROUGH, add more layers. Do not remove the first layer.",
            "⚠️ IF BLEEDING SPURTS, consider a tourniquet 2-3 inches above the wound."
        ]
        severity = "CRITICAL RISK"
    elif "fractur" in injury or "bone" in injury or "rupt" in injury or "os" in injury:
        advice = [
            "1. IMMOBILIZE the injured area. Do not attempt to realign the bone.",
            "2. APPLY A SPLINT using rigid items (rolled magazines, wood).",
            "3. APPLY ICE packs wrapped in a cloth to reduce swelling.",
            "4. ELEVATE if possible without causing more pain.",
            "⚠️ DO NOT move the person if a spinal or neck injury is suspected."
        ]
        severity = "HIGH RISK"
    else:
        advice = [
            "1. ENSURE the scene is safe for you and the patient.",
            "2. ASSESS consciousness and breathing (ABC - Airway, Breathing, Circulation).",
            "3. CALL FOR HELP using the S.O.S function if life-threatening.",
            "4. KEEP the patient calm, warm, and comfortable.",
            "⚠️ DO NOT give food or water if the patient needs surgery or is unconscious."
        ]
        severity = "ASSESSING..."

    return jsonify({"advice": advice, "severity": severity})


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