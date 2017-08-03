from datetime import datetime

def msecs_to_isodate(ts_in_msec):
    return datetime.fromtimestamp(int(ts_in_msec)/1000).isoformat()

class Earthquake(object):
    def __init__(self, record):
        props = record['properties']
        self._time = props['time']
        self._mag = props['mag']
        self._place = props['place']
        self._url = props['url']
        coords = record['geometry']['coordinates']
        self._lon, self._lat = coords[0:2]
        
    @property
    def time(self):
        return msecs_to_isodate(self._time)
        
    @property
    def magnitude(self):
        return self._mag
        
    @property
    def place(self):
        return self._place
        
    @property
    def url(self):
        return self._url
        
    @property
    def longitude(self):
        return self._lon
        
    @property
    def latitude(self):
        return self._lat