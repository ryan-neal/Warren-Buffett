"""
Module to interact with the MongoDB database.
Requires a locally running mongodb client
"""

import os
import logging

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


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

    def insert_document(self, collection_name, document):
        """Inserts a document into a given collection"""

        try:
            inserted_doc = self.db[collection_name].insert_one(document)
        except Exception:
            logging.exception("Could not write data into collection {}".format(collection_name))

        return inserted_doc

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
                self.insert_document(model.COLLECTION_NAME, document)
        return

    def data_dict_to_doc(self, model, data):
        document = {}
        for field in model.FIELDS:
            if field in data:
                document[field] = data[field]
            else:
                document[field] = ''
        return document
