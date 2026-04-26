import osmnx as ox
def get_data():
#place
    place = "Dehradun, Uttarakhand, India"

#only hospitals
    tags = {"amenity": "hospital"}

#extracting 
    hospital = ox.features_from_place(place, tags)

#only points only geometry
    hospital = hospital[hospital.geometry.type == "Point"]
    hospital['latitude'] = hospital.geometry.y
    hospital['longitude'] = hospital.geometry.x

# remove null values 
    hospital=hospital[['name', 'latitude', 'longitude']].dropna()

#print hospitals
    return hospital