import mysql.connector
from mysql.connector import errorcode

DB_CONFIG = {
    'user': 'servops',
    'password': 'servops',
    'host': '192.168.112.129',
    'database': 'db',
}

def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return None

def fetch_data():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()

        # Fetch data from Capteurs table
        cursor.execute("SELECT * FROM Capteurs")
        capteurs = cursor.fetchall()
        print("Capteurs:")
        for capteur in capteurs:
            print(capteur)

        # Fetch data from Relevés table
        cursor.execute("SELECT * FROM Relevés")
        releves = cursor.fetchall()
        print("\nRelevés:")
        for releve in releves:
            print(releve)

        cursor.close()
        conn.close()

if __name__ == "__main__":
    fetch_data()
