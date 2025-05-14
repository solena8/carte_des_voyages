from os import environ
from unittest.mock import Mock

import google.auth.credentials
from firebase_admin import initialize_app
from firebase_functions import https_fn, options
from firedantic import configure
from google.cloud.firestore import Client

from models import Place, PlaceList

app = initialize_app()

# Firestore emulator must be running if using locally.
if environ.get("FIRESTORE_EMULATOR_HOST"):
    client = Client(
        project="carte-des-voyages-tug-solena",
        credentials=Mock(spec=google.auth.credentials.Credentials)
    )
else:
    client = Client()

configure(client)


@https_fn.on_request()
def create_fake(req: https_fn.Request) -> https_fn.Response:
    # Now you can use the model to save it to Firestore
    place = Place(
        name="My Place",
        date='2032-04-23T10:20:30.400+02:30',
        city="Paris",
        country="France",
        latitude=48.8566,
        longitude=2.3522,
    )
    place.save()

    return https_fn.Response(f"New with ID {place.id} added.")


@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["post"]))
def create(req: https_fn.Request) -> https_fn.Response:
    place = Place.model_validate_json(req.data)
    place.save()
    print(place)
    return https_fn.Response(place.model_dump_json(), content_type="application/json")



@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["get"]))
def list(req: https_fn.Request) -> https_fn.Response:
    """List all places in the database."""
    places = PlaceList(root=Place.find())
    print(len(places.root))

    return https_fn.Response(places.model_dump_json(), content_type="application/json")
