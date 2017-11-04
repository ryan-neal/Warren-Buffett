import pymongo
import os
import textract
import re

DOC_PATH = os.getcwd().rsplit('Warren-Buffett', 1)[0] + os.path.join('Warren-Buffett', 'data', 'raw')

client = pymongo.MongoClient()

def initialize_database(client, dbname='BerkshireHathaway'):
	# TODO: Dump DB
	db = pymongo.database.Database(client, dbname)
	for file_name in os.listdir(DOC_PATH):
		if file_name[0] != ".":
			year = "".join(re.findall(r'\d+', file_name))
			file_text = textract.process(os.path.join(DOC_PATH, file_name))
			db['documents'].insert_one({
				'year':year,
				'text':file_text
			})
	
initialize_database(client)

