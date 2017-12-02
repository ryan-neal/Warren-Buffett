"""
Loads reports from files to the local mongo databse
"""

import os
import re
import textract
from src.data import mongodb
from src.global_settings import DATA_RAW_DIR

DOC_PATH = DATA_RAW_DIR


class Report():
    def __init__(self):
        # Required variables
        self.FIELDS = ['year', 'text']
        self.COLLECTION_NAME = 'reports'

        # optional variables
        self.UNIQUE_INDEX = 'year'

    def data_from_file(self, file_path):
        """ Process data from a file from a given path to a dictionary format """

        data = {
            'year': "".join(re.findall(r'\d+', os.path.basename(file_path))),
            'text': (textract.process(file_path, encoding='unicode_escape').decode('utf-8', 'ignore'))
        }
        return data

    def setup_db(self, db):
        """ Sets up the collection in the db to correctly accept documents"""

        db[self.COLLECTION_NAME].create_index(self.UNIQUE_INDEX, unique=True)

        return


def load_data():
    client = mongodb.DatabaseClient()
    client.connect_to_localdb()

    db_operator = mongodb.DatabaseOperations(client.db)
    model = Report()
    model.setup_db(client.db)
    db_operator.import_model_from_path(model, DOC_PATH)

    client.disconnect_client()
    return


if __name__ == '__main__':
    load_data()
