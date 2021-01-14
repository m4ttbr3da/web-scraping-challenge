from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_summary = mongo.db.mars_summary.find_one()
    return render_template("index.html", mars_summary=mars_summary)


@app.route("/scrape")
def scraper():
    mars_summary = mongo.db.mars_summary
    mars_summary_data = scrape_mars.scrape()
    mars_summary.update({}, mars_summary_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
