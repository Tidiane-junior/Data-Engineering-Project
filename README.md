# 🚀 Projet Data Engineering

**SQL · Python · Airflow · Docker · CI/CD**

## 🎯 Objectif du projet

Construire un pipeline Data Engineering complet, automatisé et industrialisable, en utilisant les bonnes pratiques modernes :

  - PostgreSQL pour le stockage
  - Python pour les transformations
  - Airflow pour l’orchestration
  - Docker pour la conteneurisation
  - CI/CD pour l’automatisation
  - Tests & Data Quality intégrés

Architecture basée sur le modèle Medallion :

  🥉 Bronze → 🥈 Silver → 🥇 Gold

## 🗺️ Roadmap du projet
### 1️⃣ Extraction des données

#### Objectif : Ingestion des données brutes.

 - Ingestion  avec l'API de Youtube (chaine : MrBeast)
 - Stockage dans PostgreSQL (schema bronze)
 - Scripts Python d’ingestion
 - Mise en place des logs

### 2️⃣ Chargement & Transformations

#### Objectif : Nettoyer et structurer les données.

 - Transformations SQL
 - Traitement Python
 - Normalisation des formats
 - Gestion des valeurs nulles
 - Suppression des doublons
 - Agrégations métiers

### 3️⃣ Data Quality Testing

#### Objectif : Garantir la fiabilité des données.

 - Vérification du nombre de lignes
 - Contrôle des valeurs nulles
 - Détection de doublons
 - Validation des schémas
 - Tests de cohérence métier

#### Outils :

  - Requêtes SQL de validation
  - Tests Python personnalisés
  - (Optionnel) Great Expectations / Soda

### 4️⃣ Tests Fonctionnels & End-to-End

#### Objectif : Valider la logique complète du pipeline.

  - Tests unitaires (Pytest)
  - Tests d’intégration
  - Tests End-to-End du DAG Airflow
  - Vérification des tables finales

### 5️⃣ Orchestration avec Airflow

#### Objectif : Automatiser le pipeline.

  - Création de DAG
  - Gestion des dépendances
  - Planification
  - Gestion des retries
  - Monitoring
  - Centralisation des logs

**Airflow orchestre** :

    Extraction → Transformation → Chargement → Tests → Validation

### 6️⃣ Conteneurisation (Docker)

#### Objectif : Rendre le projet portable et reproductible.

  - Dockerfile pour l’application
  - docker-compose pour :
    - PostgreSQL
    - Airflow
    - Services applicatifs
- Isolation des environnements
- Déploiement simplifié

### 7️⃣ CI/CD

#### Objectif : Automatiser les tests et la qualité du code.

  - GitHub Actions
  - Linting automatique
  - Lancement des tests à chaque push
  - Build d’image Docker
  - Pipeline prêt pour déploiement

## 🏗️ Architecture globale

    Données brutes
      ↓
    Schema Bronze
      ↓
    Schema Silver
      ↓
    Schema Gold
      ↓
    Analyse / BI / Machine Learning

## 🧠 Stack Technique

| Couche           | Technologie    |
| ---------------- | -------------- |
| Base de données  | PostgreSQL     |
| Langage          | Python         |
| Orchestration    | Apache Airflow |
| Conteneurisation | Docker         |
| Tests            | Pytest         |
| CI/CD            | GitHub Actions |


## 📁 Structure du projet
    Data-Engineering-project/
      ├── .github/
      │   └── workflows/          # CI/CD (GitHub Actions)
      │
      ├── dags/                   # DAGs Airflow
      │
      ├── data/                   # Données du projet (raw / processed)
      │
      ├── docker/
      │   └── postgres/           # Configuration PostgreSQL (init scripts, volumes…)
      │
      ├── include/
      │   └── soda/               # Configuration Data Quality (Soda checks)
      │
      ├── tests/                  # Tests unitaires & intégration
      │
      ├── .gitignore
      ├── docker-compose.yml      # Orchestration des services (Airflow + Postgres)
      ├── Dockerfile              # Image personnalisée Airflow
      ├── requirements.txt         # Dépendances Python
      └── README.md

## 🌐 Qu’est-ce qu’une API ?

Une **API** (Application Programming Interface) est un intermédiaire qui permet à deux applications de communiquer entre elles.

Elle définit comment demander une information et comment la recevoir, sans avoir besoin de connaître le fonctionnement interne du système.

### 🏢 Architecture API
┌──────────────────────────┐
│  Client (App / Script)    │
│  Python / Front / Service │
└─────────────┬────────────┘
              │
              │  ➜ Requête HTTP (GET/POST/PUT/DELETE)
              │
              v
┌──────────────────────────┐
│          API              │
│  Gateway / Backend API    │
│  - Auth (token)           │
│  - Validation             │
│  - Routing                │
└─────────────┬────────────┘
              │
              │  ➜ Appel service / requête SQL
              │
              v
┌──────────────────────────┐
│   Backend / Data Layer    │
│  - Business logic         │
│  - DB (PostgreSQL)        │
│  - External services      │
└─────────────┬────────────┘
              │
              │  ◄ Résultat (data / statut)
              │
              v
┌──────────────────────────┐
│          API              │
│  - Formatage (JSON)       │
│  - Codes HTTP (200/4xx)   │
└─────────────┬────────────┘
              │
              │  ◄ Réponse HTTP (JSON)
              │
              v
┌──────────────────────────┐
│  Client (App / Script)    │
└──────────────────────────┘

Pour aller plus loin : 
       https://github.com/MattTheDataEngineer/YT_ELT
