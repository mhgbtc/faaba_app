# Faaba API, une application de covoiturage au Bénin!

## Description

Faaba API est une API de covoiturage permettant à des utilisateurs de proposer et de réserver des trajets partagés à des prix abordables.

## Installation

### Avec Docker

1. Cloner le repository:

    ```
    git clone https://github.com/mhgbtc/faaba_app.git
    cd faaba_app/
    ```

2. Créer l'image docker:

    ```
    docker build -t faaba-app .
    ```

3. Démarrer le conteneur:

    ```
    docker run -p 5000:5000 faaba-app
    ```

4. L'application est maintenant accessible sur `http://localhost:5000`.

### Sans Docker

1. Cloner le repository:

    ```
    git clone https://github.com/mhgbtc/faaba_app.git
    cd faaba_app/
    ```

2. Créer un environnement virtuel et activer-le:

    ```
    python3 -m venv env
    source env/bin/activate
    ```

3. Installer les dépendances:

    ```
    pip install -r requirements.txt
    ```

4. Lancer l'application:

    ```
    cd app/
    export FLASK_APP=app.py
    export FLASK_DEBUG=true
    flask run
    ```

5. L'application est maintenant accessible sur `http://localhost:5000`.

## Utilisation

L'API Faaba propose les points de terminaisons suivants:

* `POST /register`: permet à un utilisateur de s'inscrire et d'obtenir un token JWT
* `POST /login`: permet à un utilisateur de se connecter et d'obtenir un token JWT
* `GET /rides`: retourne la liste des trajets disponibles
* `GET /rides/<ride_id>`: retourne les détails d'un trajet spécifique
* `POST /rides`: permet à un utilisateur connecté de créer un nouveau trajet
* `PUT /rides/<ride_id>`: permet à l'utilisateur ayant créé le trajet de le mettre à jour
* `DELETE /rides/<ride_id>`: permet à l'utilisateur ayant créé le trajet de le supprimer
* `GET /bookings`: retourne la liste des réservations disponibles
* `GET /bookings/<ride_id>`: retourne les détails d'une réservation spécifique
* `POST /bookings`: permet à un utilisateur connecté de créer une nouvelle réservation
* `PUT /bookings/<ride_id>`: permet à l'utilisateur ayant créé la réservation de la mettre à jour
* `DELETE /bookings/<ride_id>`: permet à l'utilisateur ayant créé la réservation de la supprimer

Pour les points de terminaisons qui nécessitent une authentification, vous devez inclure le token JWT dans le header `Authorization` avec le format suivant: Bearer <votre_token>

## Tests

Les tests sont exécutés en utilisant unittest. Pour exécuter les tests, exécutez :
`python3 test.py`.

## Quelques Exemples

1. S'inscrire:

POST /register
{
    "email" : "test7@gmail.com",
    "password" : "Test1234",
    "confirm_password" : "Test1234"
}

Réponse :
{
    "created": 5,
    "success": true,
    "token": "<votre_token>"
}

2. Se connecter

POST /login
{
    "email" : "test7@gmail.com",
    "password" : "Test1234"
}

Réponse :
{
    "logged": 5,
    "success": true,
    "token": "<votre_token>"
}

3. Obtenir la liste des trajets disponibles

GET /rides

Réponse :
{
    "rides": [
        {
            "arrival": "Calavi",
            "departure": "Porto-Novo",
            "departure_date": "Mon, 30 Jan 2023 15:45:18 GMT",
            "driver_id": 1,
            "estimated_arrival_date": "Tue, 31 Jan 2023 15:45:18 GMT",
            "id": 1,
            "seats": 1
        },
        {
            "arrival": "Cotonou",
            "departure": "Port-Louis",
            "departure_date": "Mon, 30 Jan 2023 15:45:18 GMT",
            "driver_id": 2,
            "estimated_arrival_date": "Tue, 31 Jan 2023 15:45:18 GMT",
            "id": 3,
            "seats": 5
        }
    ],
    "success": true
}

4. Option Recherche : Obtenir la liste des trajets disponibles par recherche

GET /rides
{
    "arrival": "Calavi",
    "departure": "Porto"
}

Réponse :
{
    "rides": [
        {
            "arrival": "Calavi",
            "departure": "Porto-Novo",
            "departure_date": "Mon, 30 Jan 2023 15:45:18 GMT",
            "driver_id": 1,
            "estimated_arrival_date": "Tue, 31 Jan 2023 15:45:18 GMT",
            "id": 1,
            "seats": 1
        }
    ],
    "success": true
}

### Pour les points de terminaison restants, tâchez de renseigner le token issu de l'inscription ou connexion.

Header:
Authorization: Bearer <votre token>

5. Publier un nouveau trajet

POST /rides
{
    "arrival": "Sado",
    "departure": "Gbeko",
    "departure_date": "2023-02-20 10:00:00",
    "driver_id": 4,
    "estimated_arrival_date": "2023-03-25 14:00:00",
    "seats": 1
}

Réponse : 
{
    "created": 5,
    "success": true
}

6. Faire une réservation

POST /bookings
{
    "passenger_id": 4,
    "ride_id": 1
}

Réponse :
```json
{
    "created": 3,
    "success": true
}
```

## Auteur

Mahougnon Samuel