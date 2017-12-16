import pymongo

client = pymongo.MongoClient()
db = client['BerkshireHathaway']['reports']

def create_document(year):
    """ Given a year, query MongoDB for the corresponding report """
    return db.find_one({'year':str(year)})['text'].decode('utf-8')

def clean_document(document_text):
    pass

def get_good_years():
    good_years = db.find( { "brk-returns": { '$gt':  } }, 
                                  {"year": True, "_id": False })
    lst = []
    for item in good_years:
        lst.append(item['year'])
    return(lst)

def get_bad_years():
    bad_years = db.find( { "brk-returns": { '$lt': 0 } }, 
                                 {"year": True, "_id": False })
    lst = []
    for item in bad_years:
        lst.append(item['year'])
    return(lst)

def get_brk(year):
    return db.find_one({'year': str(year)})['brk-returns']


def get_sp(year):
    return db.find_one({'year': str(year)})['s&p-returns']