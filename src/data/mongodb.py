"""
Module to interact with the MongoDB database.
Requires a locally running mongodb client
"""

import os
import logging

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# TODO: move to global
log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)


class DatabaseClient():
    def __init__(self):
        self.client = None
        self.db = None

    def connect_to_localdb(self, client_name="BerkshireHathaway"):
        # Connects to locally running db at 'mongodb://localhost:27017/'
        try:
            self.client = MongoClient()
        except ConnectionFailure:
            logging.exception("Could not connect to local MongoDB Database :(")

        self.db = self.client[client_name]

    def disconnect_client(self):
        self.client.close()


class DatabaseOperations():
    def __init__(self, db):
        self.db = db

    def insert_document(self, model, document):
        """Inserts a document into a given collection"""

        collection_name = model.COLLECTION_NAME
        collection = self.db[collection_name]
        logging.info("inserting data into collection <{}>".format(collection_name))

        # if documents can be unique, update if found
        if model.UNIQUE_INDEX:
            coll_filter = {model.UNIQUE_INDEX: document[model.UNIQUE_INDEX]}
            if collection.find_one(coll_filter):
                logging.info("updating prexisting data for {}".format(document[model.UNIQUE_INDEX]))
                update = {"$set": document}
                try:
                    collection.update_one(coll_filter, update, upsert=False)
                except Exception:
                    logging.exception("Could not write data into collection {}".format(collection_name))

                return

        # else insert new document
        logging.info("inserting new data")
        try:
            collection.insert_one(document)
        except Exception:
            logging.exception("Could not write data into collection {}".format(collection_name))

        return

    def import_model_from_path(self, model, data_path):
        """Imports multiple documents from a given path structred as one model"""

        if os.path.exists(data_path):
            file_directory = os.listdir(data_path)
        else:
            logging.error("Path {} does not exist.".format(data_path))
            raise Exception

        for file_name in file_directory:
            if file_name[0] != ".":
                file_path = os.path.join(data_path, file_name)
                document_data = model.data_from_file(file_path)
                document = self.data_dict_to_doc(model, document_data)
                self.insert_document(model, document)
        return

    def data_dict_to_doc(self, model, data):
        document = {}
        for field in model.FIELDS:
            if field in data:
                document[field] = data[field]
            else:
                document[field] = ''
        return document
