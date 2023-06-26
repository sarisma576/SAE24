import json
import mysql.connector
import paho.mqtt.client as mqtt
from datetime import datetime

cache_file = 'cache.csv'


# Fonction pour uploader les données du cache dans la base de données
def upload_cache_to_database():
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='mqtt'
        )
        cursor = conn.cursor()

        with open(cache_file, 'r') as cache:
            lines = cache.readlines()

            for line in lines:
                data = line.strip()

                # Extraction des valeurs des champs du message
                fields = {}
                for field in data.split(','):
                    key, value = field.split('=')
                    fields[key] = value

                # Convertir le format de date
                date_obj = datetime.strptime(fields['date'], '%d/%m/%Y')
                formatted_date = date_obj.strftime('%Y-%m-%d')

                capteur_query = "INSERT IGNORE INTO capteur (nom, piece) VALUES (%s, %s)"
                capteur_values = (fields['Id'], fields['piece'])
                cursor.execute(capteur_query, capteur_values)

                donnee_query = "INSERT INTO donnee (capteur_id, date, heure, temperature) VALUES (%s, %s, %s, %s)"
                donnee_values = (fields['Id'], formatted_date, fields['time'], fields['temp'])
                cursor.execute(donnee_query, donnee_values)

        # Validation des modifications dans la base de données
        conn.commit()

        # Fermeture de la connexion à la base de données
        conn.close()

        # Effacer le contenu du cache après l'upload
        with open(cache_file, 'w') as cache:
            cache.write('')

        print("Données du cache réuploadées dans la base de données")
    except mysql.connector.Error as e:
        print(f"Erreur lors de l'enregistrement dans la base de données : {e}")
        print("Impossible de réuploader les données du cache")


# Callback appelée lorsque la connexion au broker est établie
def on_connect(client, userdata, flags, rc):
    print("Connecté au broker MQTT")
    client.subscribe("IUT/Colmar2023/SAE2.04/Maison1")  # Spécifiez ici le topic auquel vous souhaitez vous abonner


# Callback appelée lorsqu'un message est reçu sur le topic auquel on est abonné
def on_message(client, userdata, msg):
    upload_cache_to_database()
    data = msg.payload.decode()  # Convertit les données reçues en chaîne de caractères
    print(data)
    # Extraction des valeurs des champs du message
    fields = {}
    for field in data.split(','):
        key, value = field.split('=')
        fields[key] = value

    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='mqtt'
        )
        cursor = conn.cursor()

        # Convertir le format de date
        date_obj = datetime.strptime(fields['date'], '%d/%m/%Y')
        formatted_date = date_obj.strftime('%Y-%m-%d')

        capteur_query = "INSERT IGNORE INTO capteur (nom, piece) VALUES (%s, %s)"
        capteur_values = (fields['Id'], fields['piece'])
        cursor.execute(capteur_query, capteur_values)

        donnee_query = "INSERT INTO donnee (capteur_id, date, heure, temperature) VALUES (%s, %s, %s, %s)"
        donnee_values = (fields['Id'], formatted_date, fields['time'], fields['temp'])
        cursor.execute(donnee_query, donnee_values)

        # Validation des modifications dans la base de données
        conn.commit()

        # Fermeture de la connexion à la base de données
        conn.close()

        print("Données enregistrées dans la base de données")
    except mysql.connector.Error as e:
        print(f"Erreur lors de l'enregistrement dans la base de données : {e}")
        print("Stockage des données dans le cache")

        # Stockage des données dans le cache
        with open(cache_file, 'a') as cache:
            cache.write(data + '\n')


# Connexion au broker MQTT
broker = "test.mosquitto.org"  # Adresse du broker MQTT
port = 1883  # Port par défaut pour MQTT

# Création d'une instance du client MQTT
client = mqtt.Client()

# Définition des callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connexion au broker MQTT
client.connect(broker, port)

# Boucle principale pour maintenir la connexion et traiter les messages reçus
client.loop_forever()
