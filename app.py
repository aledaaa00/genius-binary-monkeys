from flask import Flask, render_template

app = Flask(__name__)

<<<<<<< HEAD
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/earthquakes')
def earthquakes():
    return render_template('earthquakes.html')

@app.route('/wildfires')
def wildfires():
    return render_template('wildfires.html')

@app.route('/storms')
def storms():
    return render_template('storms.html')

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
=======
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/earthquakes")
def earthquakes():
    return render_template("earthquakes.html")


@app.route("/wildfires")
def wildfires():
    return render_template("wildfires.html")

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 152eed4c0916b339f556c52e9db9a3cbc63879e1
