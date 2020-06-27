from pymongo import MongoClient
from pymongo.errors import InvalidOperation
from t import MONGO_USERNAME, MONGO_PASSWORD


def make_mongo_client():
    client = MongoClient(
        f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@fitupyourstyle.knqya.gcp.mongodb.net/test?retryWrites=true&w=majority"
    )

    return client
