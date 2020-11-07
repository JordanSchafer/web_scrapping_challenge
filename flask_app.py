from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo
import scrape_mars

#Create an instance of Flask
app=Flask(__name__)

#Setup connection to mongodb
app.config["MONGO_URI"]="mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Create routes and render html templates
@app.route("/")
def index():

    mars_dict=mongo.db.mars_dict.find_one()

    return render_template("index.html",mars=mars_dict)

@app.route("/scrape")
def scrape():

    mars_dict = mongo.db.mars_dict
    mars_data=scrape_mars.scrape()

    mars_dict.update({},mars_data,upsert=True)
    return redirect("/",code=302)

if __name__=="__main__":
    app.run(debug=True)