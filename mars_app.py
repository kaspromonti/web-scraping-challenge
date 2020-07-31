from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# creating connection and db called Mars_app???
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars_app"
mongo = PyMongo(app)


# mars_info = the collection within the db?? is db established by the connection above?
# anywhere I reference 'mars.xxxx' in the html should pull in mars_info collection from mongo?

@app.route("/")
def index():
    mars_info = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars_info)

# data is the dict from the scrap file scrape_mars using the scrape_all function created in scrape file?
# updating the db.collection (named above) with data info? why don't we use the variable names of mars_info and Mars_app?
@app.route("/scrape")
def scraper():
    data = scrape_mars.scrape_all()  
    mongo.db.collection.update({}, data, upsert=True) 
    print(data)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
