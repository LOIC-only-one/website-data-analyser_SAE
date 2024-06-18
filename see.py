import mysql.connector
from mysql.connector import errorcode

DB_CONFIG = {
    'user': 'servops',
    'password': 'servops',
    'host': '192.168.112.129',
    'database': 'db',
}

def connect_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def fetch_data():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Capteurs")
        capteurs = cursor.fetchall()
        print("Capteurs:")
        for capteur in capteurs:
            print(capteur)

        cursor.execute("SELECT * FROM Relevés")
        releves = cursor.fetchall()
        print("\nRelevés:")
        for releve in releves:
            print(releve)

        cursor.close()
        conn.close()

if __name__ == "__main__":
    fetch_data()
