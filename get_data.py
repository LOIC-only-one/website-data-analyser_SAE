import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

BROKER_URL_1 = "test.mosquitto.org"
BROKER_URL_2 = "broker.hivemq.com"
TOPICS = [
    "IUT/Colmar2024/SAE2.04/Maison1",
    "IUT/Colmar2024/SAE2.04/Maison2"
]

DB_CONFIG = {
    'user': 'servops',
    'password': 'servops',
    'host': '192.168.112.129',
    'database': 'db',
}

def connect_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def init_db():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Capteurs (
                capteur_id VARCHAR(50) PRIMARY KEY,
                nom VARCHAR(100) UNIQUE NOT NULL,
                piece VARCHAR(50) NOT NULL,
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Relevés (
                releve_id INT PRIMARY KEY AUTO_INCREMENT,
                capteur_id VARCHAR(50) NOT NULL,
                timestamp DATETIME NOT NULL,
                temperature FLOAT,
                FOREIGN KEY (capteur_id) REFERENCES Capteurs(capteur_id)
            )
        ''')
        conn.commit()
        conn.close()

def convert_to_mysql_datetime(date_str, time_str):
    datetime_str = f"{date_str} {time_str}"
    return datetime.strptime(datetime_str, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

def insert_data_to_db(data_entry):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()

        capteur_id = data_entry["id"]
        piece = data_entry["piece"]
        timestamp = convert_to_mysql_datetime(data_entry["date"], data_entry["time"])
        temperature = data_entry["temperature"]

        cursor.execute('SELECT COUNT(*) FROM Capteurs WHERE capteur_id = %s', (capteur_id,))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO Capteurs (capteur_id, nom, piece)
                VALUES (%s, %s, %s)
            ''', (capteur_id, f"Capteur {capteur_id}", piece))
            conn.commit()

        data_entry_db = (capteur_id, timestamp, temperature)
        cursor.execute('''
            INSERT INTO Relevés (capteur_id, timestamp, temperature)
            VALUES (%s, %s, %s)
        ''', data_entry_db)
        conn.commit()
        conn.close()





############################## MQTT ##############################




def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    for topic in TOPICS:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    payload = msg.payload.decode()
    attributes = {}
    for item in payload.split(','):
        key, value = item.split('=')
        attributes[key] = value

    data_entry = {
        "topic": msg.topic,
        "id": attributes.get("Id"),
        "piece": attributes.get("piece"),
        "date": attributes.get("date"),
        "time": attributes.get("time"),
        "temperature": float(attributes.get("temp"))
    }

    insert_data_to_db(data_entry)

def main():
    init_db()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_URL_1, 1883, 60)
    client.loop_start()

    client_2 = mqtt.Client()
    client_2.on_connect = on_connect
    client_2.on_message = on_message
    client_2.connect(BROKER_URL_2, 1883, 60)
    client_2.loop_start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        client.loop_stop()
        client_2.loop_stop()
        print("Script terminated")

if __name__ == "__main__":
    main()
