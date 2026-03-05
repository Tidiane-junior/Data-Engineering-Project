# Importer les modules necessaire
from dotenv import load_dotenv
import requests # requests pour faire des requêtes HTTP
import json # json pour gérer les données JSON
import os # os pour gérer les variables d'environnement
from dotenv import load_dotenv # pour charger les variables d'environnement à partir d'un fichier .env

load_dotenv(dotenv_path ="./.env") # Charger les variables d'environnement à partir du fichier .env

API_KEY = os.getenv("API_KEY") # Récupérer la clé API à partir des variables d'environnement
channel_handle = "MrBeast" # La chaine Youtube dont on veut récupérer les statistiques

def get_playlisT_Id():

    try :
        # Construire l'URL de la requête depuis YouTube API pour obtenir les détails du canal YouTube
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={API_KEY}"

        response = requests.get(url)

        response.raise_for_status() # Vérifier si la requête a réussi, sinon lever une exception
        
        data = response.json()

        # J'ultilise json.dumps pour formater les données JSON avec une meilleure lisibilité
        # print(json.dumps(data, indent = 4)) 

        # l'extension *Json Crack* est utille pour visualiser les données JSON de manière plus claire et organisée 

        # Je recupère les éléments de la réponse JSON pour accéder aux détails du canal YouTube
        channel_items = data["items"][0]
        # Je récupère l'identifiant de la playlist des vidéos téléchargées 
        channel_playlisId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        print(channel_playlisId) 

        return channel_playlisId
    except requests.exceptions.RequestException as e:
        raise e
    
if __name__ == "__main__":
    get_playlisT_Id()

