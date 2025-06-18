from flask import Flask, render_template, request
from utils import get_site_summary

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        site_id = request.form["site_id"]
        channel_id = request.form["channel_id"]
        result = get_site_summary(site_id, channel_id)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
