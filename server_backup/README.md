uvicorn functions.main:app --reload

DOC : http://127.0.0.1:8000/docs#/


# Documentation FastAPI pour le projet

## Introduction

Ce projet utilise FastAPI pour créer une API RESTful qui gère des données liées à des lieux. Nous avons plusieurs routes pour ajouter, lire et supprimer des lieux dans une base de données SQLite en utilisant SQLAlchemy comme ORM. Pydantic est utilisé pour valider les données entrantes et sortantes.

## Structure des fichiers

- **main.py** : Point d'entrée de l'application FastAPI. Configure l'API et inclut les routes.
- **models/model_places.py** : Définit la structure de la table `places` dans la base de données.
- **schemas/schema_places.py** : Contient les modèles Pydantic pour valider et transformer les données.
- **services/service_places.py** : Contient la logique métier pour créer un nouveau lieu.
- **dependencies.py** : Définit une fonction pour gérer les sessions de la base de données.
- **database.py** : Gère la connexion à la base de données.

## Routes

### 1. Route POST `/places/` - Créer un lieu

#### Fonction : `create_place`

Cette route permet de créer un nouveau lieu dans la base de données.

- **Méthode HTTP** : `POST`
- **Corps de la requête** : Doit contenir un objet JSON conforme au modèle `PlaceCreate`.
- **Réponse** : Retourne l'objet créé, avec les informations de ce lieu dans un format conforme au modèle `Place`.

#### Explication

Lorsque la route `POST /places/` est appelée :
1. La fonction `create_place` reçoit un objet JSON avec les données d'un lieu, qui est automatiquement validé par Pydantic avec le modèle `PlaceCreate`.
2. Ces données sont ensuite envoyées à la fonction `create_new_place` du service, qui s'occupe de les ajouter à la base de données.
3. Le lieu créé est renvoyé dans la réponse, avec une structure de données conforme au modèle `Place`.

#### Exemple de requête :

```json
{
  "name": "New Place",
  "date": "2025-02-06T10:00:00",
  "city": "Nantes",
  "country": "France",
  "latitude": 47.2184,
  "longitude": -1.5536,
  "image": null
}
```

#### Exemple de réponse :

```json
{
  "id": 1,
  "name": "New Place",
  "date": "2025-02-06T10:00:00",
  "city": "Nantes",
  "country": "France",
  "latitude": 47.2184,
  "longitude": -1.5536,
  "image": null
}
```

---

### 2. Route GET `/places/` - Lire les lieux

#### Fonction : `read_places`

Cette route permet de récupérer la liste de tous les lieux enregistrés dans la base de données.

- **Méthode HTTP** : `GET`
- **Réponse** : Retourne une liste d'objets JSON contenant les informations des lieux, dans un format conforme au modèle `Place`.

#### Explication

Lorsque la route `GET /places/` est appelée :
1. La fonction `read_places` interroge la base de données pour obtenir tous les lieux stockés.
2. Les données sont ensuite formatées dans un tableau et renvoyées dans la réponse, avec un format conforme au modèle `Place` de Pydantic.

#### Exemple de réponse :

```json
[
  {
    "id": 1,
    "name": "Place 1",
    "date": "2025-02-06T10:00:00",
    "city": "Nantes",
    "country": "France",
    "latitude": 47.2184,
    "longitude": -1.5536,
    "image": null
  },
  {
    "id": 2,
    "name": "Place 2",
    "date": "2025-02-07T10:00:00",
    "city": "Paris",
    "country": "France",
    "latitude": 48.8566,
    "longitude": 2.3522,
    "image": null
  }
]
```

---

### 3. Route DELETE `/places/{id}` - Supprimer un lieu

#### Fonction : `delete_place`

Cette route permet de supprimer un lieu en fonction de son ID.

- **Méthode HTTP** : `DELETE`
- **Paramètre** : `id` : L'ID du lieu à supprimer.
- **Réponse** : Retourne un message de succès après la suppression.

#### Explication

Lorsque la route `DELETE /places/{id}` est appelée :
1. La fonction `delete_place` cherche le lieu avec l'ID fourni dans la base de données.
2. Si le lieu est trouvé, il est supprimé de la base de données.
3. Un message de succès est renvoyé, confirmant la suppression.

#### Exemple de réponse :

```json
{
  "message": "Place deleted successfully"
}
```

---

## Schémas Pydantic

### 1. `PlaceCreate` (pour les requêtes POST)

Le modèle `PlaceCreate` est utilisé pour valider les données lorsqu'un utilisateur crée un nouveau lieu via la route POST.

```python
class PlaceCreate(BaseModel):
    name: str
    date: datetime
    city: str
    country: str
    latitude: float
    longitude: float
    image: Optional[bytes] = None
```

### 2. `Place` (pour les requêtes GET)

Le modèle `Place` est utilisé pour valider et formater les données renvoyées par la route GET.

```python
class Place(BaseModel):
    id: int
    name: str
    date: datetime
    city: str
    country: str
    latitude: float
    longitude: float
    image: Optional[bytes] = None
```

---

## Conclusion

Ce projet FastAPI utilise les principes du RESTful API en combinant SQLAlchemy pour la gestion de la base de données, Pydantic pour la validation des données, et FastAPI pour la gestion des routes et la création d'une documentation interactive. Grâce à la validation avec Pydantic, les données sont assurées d'être correctes avant d'être envoyées à la base de données ou renvoyées dans les réponses API.
