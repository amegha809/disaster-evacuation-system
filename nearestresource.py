from database import connect_datab
import math
import pyttsx3
from location import get_loc

# voice alert
engine = pyttsx3.init()

def find_nearest(place, choice):

    # user latitude and longitude
    lat_u, lon_u = get_loc(place)

    if lat_u is None:
        return "Location not found!"

    # decision code for selecting table
    if choice == 1:
        table = "first_aid"
        label = "First Aid Center"
    elif choice == 2:
        table = "hospital"
        label = "Hospital"
    elif choice == 3:
        table = "shelters"
        label = "Shelter"
    else:
        return "Invalid choice"

    # distance formula (Haversine)
    def distance_calculate(lat1, lon1, lat2, lon2):
        R = 6371

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    # connecting database
    conn = connect_datab()
    cursor = conn.cursor()

    if table == "first_aid":
        query = "SELECT name, latitude, longitude FROM first_aid WHERE available = TRUE"

    elif table == "shelters":
        query = "SELECT name, latitude, longitude FROM shelters WHERE capacity > 0"

    else:
        query = f"SELECT name, latitude, longitude FROM {table}"

    cursor.execute(query)
    data = cursor.fetchall()

    nearest_name = None
    nearest_lat = None
    nearest_lon = None
    min_distance = float('inf')

    for name, lat, lon in data:

        dist = distance_calculate(lat_u, lon_u, lat, lon)

        if dist < min_distance:
            min_distance = dist
            nearest_name = name
            nearest_lat = lat
            nearest_lon = lon

    # shelter capacity update
    if table == "shelters":
        update_query = "UPDATE shelters SET capacity = capacity - 1 WHERE name = %s"
        cursor.execute(update_query, (nearest_name,))
        conn.commit()

    # distance in meters or km
    if min_distance < 1:
        distance_text = f"{round(min_distance * 1000)} meters"
    else:
        distance_text = f"{round(min_distance,2)} km"

    # voice message
    msg = f"Nearest {label} is {nearest_name} which is at a distance of approximately {distance_text} from your current location"

    engine.setProperty('rate',150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    engine.say(msg)
    engine.runAndWait()

    cursor.close()
    conn.close()

    result_text = f"Nearest {label}: {nearest_name}\nDistance: {distance_text}"

    return result_text, nearest_name, nearest_lat, nearest_lon