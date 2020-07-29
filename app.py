from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():
    # Store the entire team collection in a list
    scraping_to_html = mongo.db.scraping.find_one()
    print(scraping_to_html)

    # Return the template with the teams list passed in
    return render_template('index.html', scraping_to_html=scraping_to_html)
    

@app.route("/scrape")
def scrape_route():
    scrape_db =  mongo.db.scraping
    scrape_data = scrape_mars.scrape()
    scrape_db.update({}, scrape_data, upsert=True)
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)