
# Dependencies
from flask import Flask, redirect, render_template
from flask_pymongo import PyMongo
import scrape_NASA

#############################################################
# Flask Setup
#############################################################
app = Flask(__name__)

#############################################################
# Setup Mongo connection
#############################################################
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsDB"
mongo = PyMongo(app)


#############################################################
# Flask Home Page
#############################################################
@app.route("/")
def welcome():
    mongoCurrent = mongo.db.scraped_Results.find_one()
    for key in mongoCurrent:
        featured_title = key['featured_title']
        featured_teaser = key['featured_teaser']
        featured_link = key['featured_link']
        featured_image_url = key['featured_image_url']
        mars_weather = key['mars_weather']
        marsHTML = key['marsHTML']
        timestamp = key['timestamp']
        hemisphere_img = key['hemisphere_images']


    return render_template("index.html", featured_title = featured_title,
                                        featured_teaser = featured_teaser,
                                        featured_link = featured_link,
                                        featured_image_url = featured_image_url,
                                        mars_weather = mars_weather,
                                        marsHTML = marsHTML,
                                        timestamp = timestamp,
                                        hemisphere = hemisphere_img
                                        )

# 

#############################################################
# Flask / Scrape Function
#############################################################
@app.route("/scrape")
def scrapeNow():
    mongoCurrent = mongo.db.scraped_Results
    mongoCurrentData = scrape_NASA.scrape()
    mongoCurrent.update({}, mongoCurrentData, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

