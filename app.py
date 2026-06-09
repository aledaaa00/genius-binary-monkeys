from flask import Flask, render_template

app = Flask(__name__)

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