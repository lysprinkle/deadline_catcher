# app.py
from flask import Flask, render_template, send_file, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scraper import scrape_canvas_data
import os

app = Flask(__name__)
driver = None
base_url = "https://canvas.illinois.edu"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_scraping():
    global driver
    try:
        if driver is None:
            options = Options()
            options.add_argument("--start-maximized")
            driver = webdriver.Chrome(options=options)
            driver.get(base_url)

        # Try scraping directly — if cookies are valid, skip login
        result_file = scrape_canvas_data(driver, base_url)
        if not result_file:
            # Not logged in → open Canvas login page
            driver.get(base_url)
            return jsonify({"status": "login_required"})

        return jsonify({"status": "ok", "download_url": "/download"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/download")
def download():
    filepath = "canvas_data.json"
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "No file found", 404

if __name__ == "__main__":
    app.run(debug=True)

