"""
Module to interact with the MongoDB database.

Requires a locally running database

"""
import logging

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class DatabaseClient():
    def __init__(self):
        self.client = None
        self.db = None

    def connect_to_localdb(self):
        # Connects to locally running db at 'mongodb://localhost:27017/'
        try:
            self.client = MongoClient()
        except ConnectionFailure:
            logging.exception("Could not connect to local MongoDB Database :(")

        self.db = self.client['warren-buffet']


class DatabaseOperations():
    def __init__(self, db):
        self.db = db
        self.collection = db.reports

    def format_report(self, report):
        return

    def insert_report(self, report):
        return

    def import_from_file(self):
        return

    def get_all_reports(self):
        return
