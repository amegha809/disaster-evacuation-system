import mysql.connector
def connect_datab():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="m1e2g3h4a5",
        database="disaster_evacuation"
    )
    return conn