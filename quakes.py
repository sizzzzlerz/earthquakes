from flask import Flask, render_template
import json
from datetime import datetime
import urllib2
from earthquake import Earthquake

USGS_PAST_DAY_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
#USGS_PAST_DAY_URL = "file:all_day.geojson"

def load_earthquake_data():
    fp = urllib2.urlopen(USGS_PAST_DAY_URL)
    data = fp.read()
    if not data:
        return None
    quakes_json = json.loads(data)
    quakes =  [Earthquake(f) for f in quakes_json['features']]
    return quakes
        
app = Flask(__name__)

@app.route("/")
def get_quakes():
    quakes = load_earthquake_data()
    #print quakes['features']
    if quakes is None:
        return

    quakes.sort( reverse=True, key=lambda r:r.magnitude )
   
    return render_template('quakes.html', earthquakes=quakes)

@app.context_processor
def my_utility_processor():
    def isodate(ts_in_msec):
        return msecs_to_isodate(ts_in_msec)
    
    def coordinates(geo):
        lon,lat,depth = geo
        return "{:8.3f} {:7.3f}".format(lon,lat)
        
    return dict(isodate=isodate, coordinates=coordinates)
    
    
if __name__ == "__main__":
    app.run(port=5000, debug=True)