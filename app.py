from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Google Apps Script Web App URL used to save submissions to Google Sheets.
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwmheXODme6_rP8ivoF-26yTPxpG3q7PigkGzRXBweWSbVs5B-lsjpSLPGI-OyJgRYo/exec"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    data = {
        "date": request.form.get("date", ""),
        "supervisor": request.form.get("supervisor", ""),
        "promoter": request.form.get("promoter", ""),
        "store": request.form.get("store", ""),
        "attendance": request.form.get("attendance", ""),
        "shift": request.form.get("shift", "")
    }

    required = ["date", "supervisor", "promoter", "store", "attendance"]
    if any(not data[x] for x in required):
        return "Please fill all required fields. <a href='/'>Go back</a>", 400

    try:
        response = requests.post(GOOGLE_SCRIPT_URL, json=data, timeout=20)
        response.raise_for_status()
        result = response.json()

        if not result.get("success"):
            return f"Google Sheet error: {result.get('error', 'Unknown error')}", 500

        return redirect(url_for("success"))

    except Exception as e:
        return f"Could not save to Google Sheet: {e}<br><br><a href='/'>Go back</a>", 500


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
