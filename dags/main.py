from airflow import DAG
import pendulum
from datetime import datetime, timedelta, tzinfo
from api.video_stats import get_playlist_id, get_video_ids, extract_video_data, save_to_json

# Je définis le fuseau horaire local pour Paris
local_tz = pendulum.timezone("Europe/Paris")
# Le site Timezonedb.com : ressource utile pour trouver les fuseaux horaires et leurs identifiants

# Je définis les arguments par défaut pour le DAG, y compris le fuseau horaire et la date de début
default_args = {
    "owner": "dataengineer", # Je définis le propriétaire du DAG, qui est généralement l'équipe ou la personne responsable de son exécution
    "depends_on_past": False, # Je spécifie que les tâches de ce DAG ne dépendent pas de l'exécution réussie des tâches précédentes, ce qui signifie qu'elles peuvent s'exécuter indépendamment les unes des autres
    "email_on_failure": False, # Je choisis de ne pas recevoir d'e-mails en cas d'échec des tâches, ce qui peut être utile pour éviter les notifications excessives, surtout si le DAG est exécuté fréquemment ou s'il y a des échecs temporaires attendus
    "email_on_retry": False, # Je choisis de ne pas recevoir d'e-mails en cas de tentative de réexécution des tâches, ce qui peut être utile pour éviter les notifications excessives, surtout si le DAG est exécuté fréquemment ou s'il y a des échecs temporaires attendus
    "email": "data@engineer.com",
    # "retries": 1, # Je définis le nombre de tentatives de réexécution des tâches en cas d'échec, ce qui peut être utile pour gérer les erreurs temporaires ou les problèmes de connectivité
    # "retry_delay": timedelta(minutes=5), # Je définis le délai entre les tentatives de réexécution des tâches, ce qui peut être utile pour éviter les échecs répétés en cas de problèmes temporaires
    "max_active_runs": 1, # Je limite le nombre d'exécutions simultanées du DAG à 1, ce qui signifie que si une instance du DAG est déjà en cours d'exécution, les nouvelles instances seront mises en file d'attente jusqu'à ce que l'instance en cours soit terminée
    "degrun_timeout": timedelta(hours=1), # Je définis un délai d'exécution maximum pour le DAG, ce qui signifie que si le DAG prend plus de temps que ce délai pour s'exécuter, il sera automatiquement arrêté pour éviter les exécutions prolongées ou bloquées
    "start_date": datetime(2024, 6, 1, tzinfo=local_tz), # Je définis la date de début du DAG, ce qui signifie que le DAG commencera à s'exécuter à partir de cette date. En utilisant le fuseau horaire local, je m'assure que les exécutions du DAG sont alignées avec l'heure locale.
    # "end_date": datetime(2030, 12, 31, tzinfo=local_tz)
}

with DAG(
    dag_id = "produce_json_data", # Je définis l'identifiant du DAG, qui est un nom unique utilisé pour identifier ce DAG dans Airflow
    default_args = default_args,
    description = "DAG pour produire des données JSON",
    schedule = "0 14 * * *", # Je définis la planification du DAG en utilisant une expression cron, ce qui signifie que le DAG s'exécutera tous les jours à 14h00 (heure locale)    
    catchup = False

) as dag : 
    
    # Je defini les tâches du DAG en utilisant les fonctions importées depuis le module api.video_stats. 
    # Chaque tâche est définie comme une fonction décorée avec @task, 
    # ce qui permet à Airflow de les exécuter en tant que tâches indépendantes dans le DAG.
    playliist_id = get_playlist_id()
    video_ids = get_video_ids(playliist_id)
    extract_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(extract_data)

    # Je définis les dépendances entre les tâches en utilisant l'opérateur >>, 
    # ce qui signifie que chaque tâche doit être exécutée après la tâche précédente. 
    # Cela garantit que les tâches sont exécutées dans le bon ordre, 
    # en respectant les dépendances logiques entre elles.
    playliist_id >> video_ids >> extract_data >> save_to_json_task

# Nous venons de créer notre premier DAG Airflow qui récupère les statistiques des vidéos d'une chaîne YouTube,
