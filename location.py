from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut

def get_loc(place_input):
    geolocator = Nominatim(user_agent="disaster_project")

    query = place_input.strip() + ", Dehradun, Uttarakhand, India"

    try:
        location = geolocator.geocode(query, timeout=10)

        if location:
            return location.latitude, location.longitude
        else:
            return None, None

    except (GeocoderUnavailable, GeocoderTimedOut):
        return None, None