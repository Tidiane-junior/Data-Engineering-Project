# Importer les modules necessaire
import requests # pour faire des requêtes HTTP
import os # pour gérer les variables d'environnement
from dotenv import load_dotenv # pour charger les variables d'environnement à partir d'un fichier .env
import json
from datetime import date

from airflow.decorators import task
from airflow.models import variable

load_dotenv(dotenv_path ="./.env") # Charger les variables d'environnement à partir du fichier .env
API_KEY = os.getenv("API_KEY") # Récupérer la clé API à partir des variables d'environnement
CHANNEL_HANDLE = "MrBeast" # La chaine Youtube dont on veut récupérer les statistiques
maxResults = 50 # Le nombre maximum de résultats à récupérer pour les vidéos

@task
def get_playlist_id():

    try :
        # Construire l'URL de la requête depuis YouTube API pour obtenir les détails du canal YouTube
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

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
    

@task
def get_video_ids(playlistId):
    video_ids = []

    pageToken = None

    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"


    try : 
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"

            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            for item in data.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)

            pageToken = data.get("nextPageToken")

            if not pageToken:
                break

        return video_ids
    
    except requests.exceptions.RequestException as e:
        raise e


@task
def batch_list(video_ids_list, batch_size):
    for video_id in range(0, len(video_ids_list), batch_size):
        yield video_ids_list[video_id : video_id + batch_size]

@task
def extract_video_data(video_ids):
    extracted_data = []
   
    try : 
        # YouTube API a une limite de 50 vidéos par requête, donc je divise la liste des video_ids en batches de 50 pour faire plusieurs requêtes si nécessaire
        for batch in batch_list(video_ids, maxResults):
            video_ids_str = ",".join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"
            
            response = requests.get(url)

            response.raise_for_status()

            data = response.json()
             
            for item in data.get("items", []): 
                video_id = item["id"]
                snippet = item["snippet"]
                contentDetails = item["contentDetails"]
                statistics = item["statistics"]
            
                # Je recupère les infos pertinentes pour chaque vidéo et les stocke dans un dictionnaire
                video_data = {
                    "video_id": video_id,
                    "title": snippet["title"],
                    "publishedAt": snippet["publishedAt"],
                    "duration": contentDetails["duration"],
                    "viewCount": statistics.get("viewCount"),
                    "likeCount": statistics.get("likeCount"),
                    "commentCount": statistics.get("commentCount"),   
                }
                
                extracted_data.append(video_data)

        return extracted_data
    
    except requests.exceptions.RequestException as e:
        raise e

@task
def save_to_json(extracted_data):
    file_path = f"./data/YT_data_{date.today()}.json"

    with open(file_path, "w", encoding="utf-8") as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    playlistId = get_playlist_id()
    video_ids = get_video_ids(playlistId)
    video_data = extract_video_data(video_ids) 
    save_to_json(video_data)
  