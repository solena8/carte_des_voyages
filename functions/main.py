from os import environ
from unittest.mock import Mock

import google.auth.credentials
from firebase_admin import initialize_app
from firebase_functions import https_fn, options
from firedantic import configure
from google.cloud.firestore import Client
from typing import List

from pydantic import RootModel
from firedantic import Model
from datetime import datetime
import json
from google.cloud import storage
import uuid


# from models import Place, PlaceList

class Place(Model):
    __collection__ = "places"
    name: str
    date: datetime
    city: str
    country: str
    latitude: float
    longitude: float
    # image_url: str


class PlaceList(RootModel):
    root: List[Place]


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
    if req.method == "OPTIONS":
        return https_fn.Response("", status=200)

    form = req.form
    # file = req.files.get("image")
    #
    # if not file:
    #     print("No file received in request.files")
    #     print("Available files:", list(req.files.keys()))
    #     print("Form data:", dict(form))
    #     return https_fn.Response("Image is required", status=400)

    # Upload de l'image dans Firebase Storage
    # bucket_name = "carte-des-voyages-tug-solena.appspot.com"
    # client = storage.Client()
    # bucket = client.bucket(bucket_name)
    #
    # unique_name = f"{uuid.uuid4()}.jpg"
    # blob = bucket.blob(f"places/{unique_name}")
    # blob.upload_from_string(file.read(), content_type=file.content_type)
    # blob.make_public()
    # image_url = blob.public_url

    place = Place(
        name=form["name"],
        date=form["date"],
        city=form["city"],
        country=form["country"],
        latitude=float(form["latitude"]),
        longitude=float(form["longitude"]),
        # image_url=image_url,
    )
    place.save()
    return https_fn.Response(place.model_dump_json(), content_type="application/json")


@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["get"]))
def list(req: https_fn.Request) -> https_fn.Response:
    places = PlaceList(root=Place.find())
    print(len(places.root))

    return https_fn.Response(places.model_dump_json(), content_type="application/json")


@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["delete"]))
def delete(req: https_fn.Request) -> https_fn.Response:
    place_id = req.args.get("id")

    if not place_id:
        return https_fn.Response("Missing id in query params", status=400)

    place = Place.get_by_id(place_id)
    if place:
        place.delete()
        return https_fn.Response(place.model_dump_json(), content_type="application/json")
    else:
        return https_fn.Response(f"No place found with id {place_id}", status=404)


@https_fn.on_request(cors=options.CorsOptions(cors_origins="*", cors_methods=["get"]))
def stats(req: https_fn.Request) -> https_fn.Response:
    all_places = Place.find()
    total_entries = len(all_places)

    total_countries = {place.country for place in all_places}
    unique_countries = len(total_countries)

    stats_data = {
        "totalEntries": total_entries,
        "uniqueCountries": unique_countries,
    }
    return https_fn.Response(
        json.dumps(stats_data),
        content_type="application/json"
    )
