from database import connect_datab 
from resource import get_data

def insert_hospital_data():
    conn = connect_datab()
    cursor = conn.cursor()

    hospital_data = get_data()

    for index, row in hospital_data.iterrows():
        query = "INSERT INTO hospital (name, latitude, longitude) VALUES (%s, %s, %s)"
        values = (row['name'], row['latitude'], row['longitude'])
        cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()

    return "Data inserted successfully!" 