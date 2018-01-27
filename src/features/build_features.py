import parse
from src.data import query

def passive_voice_percent(start_year, end_year):
    exp = [parse.generate_expression('passive_voice')]
    return [(year, parse.expression_percent(query.create_document(year), exp))
            for year in range(start_year, end_year)]

def main():
    #pv = get_phrases(create_document(1990), [generate_expression('passive_voice')])
    #print('\n'.join(': '.join(tup) for tup in pv))
    print(passive_voice_percent(2000, 2017))


if __name__ == '__main__':
    main()