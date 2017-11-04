"""
Loads reports from files to the local mongo databse
"""

import os
import re
import textract

import mongodb

DOC_PATH = os.getcwd().rsplit('Warren-Buffett', 1)[0] + os.path.join('Warren-Buffett', 'data', 'raw')


class Report():
    def __init__(self, year, text):
        self.FIELDS = ['year', 'text']
        self.COLLECTION_NAME = 'reports'

    def process_from_file(self, file_name):
        file_path = os.path.join(DOC_PATH, file_name)
        year = "".join(re.findall(r'\d+', file_name))
        file_text = textract.process(file_path)

        report = {
            'year': year,
            'text': file_text
        }
        return report


def load_data():
    client = mongodb.DatabaseClient()
    client.connect_to_localdb()

    db_operator = mongodb.DatabaseOperations(client.db)
    model = Report()
    db_operator.import_model_from_path(model, DOC_PATH)

    client.disconnect_client()
    return


if __name__ == '__main__':
    load_data()
