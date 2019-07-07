from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Flask
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_mission")



@app.route('/')
def home():

    mars_info = mongo.db.collection.find_one()

    return render_template('index.html', mars_info=mars_info)


@app.route('/scrape')
def index():
    
    mars_data = scrape_mars.scrape()

    mongo.db.collection.update({}, mars_data, upsert=True)

    return redirect("/")
    


if __name__ == "__main__":
    app.run(debug=True)