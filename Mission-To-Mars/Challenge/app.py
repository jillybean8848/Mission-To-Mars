from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrapingchallenge


app = Flask(__name__) 

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars_retrieved_data = mongo.db.mars.find_one()
   return render_template("index_mm.html", mars=mars_retrieved_data)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scrapingchallenge.scrape_all()
   mars.update({},mars_data, upsert=True)
   return redirect("/")

if __name__ == "__main__":
   app.run(debug=True)