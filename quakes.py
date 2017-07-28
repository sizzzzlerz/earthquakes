from flask import Flask, render_template
import json
from datetime import datetime
import urllib2

USGS_PAST_DAY_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

def load_earthquake_data():
    fp = urllib2.urlopen(USGS_PAST_DAY_URL)
    data = fp.read()
    if not data:
        return None
    quakes = json.loads(data)
    return quakes
 
def sort_by_mag(recA, recB):
    '''
    Compares the magintudes of two records and returns value based on one
    being less than, equal to, or greater than the other
    
    Note the comparisons are done reversed so that the larger magnitude will
    precede the lesser.
    '''
    
    magA = recA['properties']['mag']
    magB = recB['properties']['mag']
    if magA > magB:
        return -1
    elif magA < magB:
        return 1
    else:
        return 0
        
app = Flask(__name__)

@app.route("/")
def get_quakes():
    quakes = load_earthquake_data()
    #print quakes['features']
    if quakes is None:
        return
    
    features = sorted(quakes['features'],cmp=sort_by_mag)
    return render_template('quakes.html', features=features)

@app.context_processor
def my_utility_processor():
    def isodate(ts_in_msec):
        return datetime.fromtimestamp(int(ts_in_msec)/1000.).isoformat()
    
    def coordinates(geo):
        lat,lon,depth = geo
        return dict(latitude=lat, longitude=lon)
        
    return dict(isodate=isodate, coordinates=coordinates)
    
    
if __name__ == "__main__":
    app.run(port=5000, debug=True)