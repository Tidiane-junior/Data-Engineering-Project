# Importer les modules necessaire
import requests # requests pour faire des requêtes HTTP
import json # json pour gérer les données JSON

# Définir la clé API et le nom d'utilisateur du canal YouTube
API_KEY = "AIzaSyBqcM8cdBb7vI5mAkV0EJ4gGx8dOq8WRew"
channel_handle = "MrBeast"

def get_playlisT_Id():

    try :
        # Construire l'URL de la requête depuis YouTube API pour obtenir les détails du canal YouTube
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={API_KEY}"

        # Faire la requête GET à l'API YouTube et stocker la réponse dans une variable data
        response = requests.get(url)

        response.raise_for_status() # Vérifier si la requête a réussi, sinon lever une exception
        
        data = response.json()

        # J'ultilise json.dumps pour formater les données JSON avec une meilleure lisibilité
        # print(json.dumps(data, indent = 4)) 

        # l'extension *Json Crack* est utille pour visualiser les données JSON de manière plus claire et organisée 

        # Je recupère les éléments de la réponse JSON pour accéder aux détails du canal YouTube
        channel_items = data["items"][0]
        # Je récupère l'identifiant de la playlist des vidéos téléchargées du canal YouTube à partir des détails du canal
        channel_playlisId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        # print(channel_playlisId) # Afficher l'identifiant de la playlist des vidéos téléchargées du canal YouTube

        return channel_playlisId
    except requests.exceptions.RequestException as e:
        raise e
    
if __name__ == "__main__":
    get_playlisT_Id()

