import re
import os

from urllib.request import urlopen
from bs4 import BeautifulSoup
from src.global_settings import DATA_DIR

SAVE_DIRS = {
    'Buffett': os.path.join(DATA_DIR, 'raw')
}


def check_file_integrity():
    return


def scrape_buffett(save_dir=SAVE_DIRS['Buffett']):
    # create the directory if it does not currently exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    header = 'http://www.berkshirehathaway.com/letters/'
    page = urlopen(header + '/letters.html')
    soup = BeautifulSoup(page.read(), 'lxml')
    tags = soup.findAll('a', {'href': re.compile('.*\.(html)|(pdf)')})

    file_names = map(lambda tag: tag['href'], tags)

    for file_name in file_names:
        file_path = os.path.join(save_dir, file_name)
        if os.path.exists(file_path):
            continue  # we already scraped this

        content = urlopen(header + file_name).read()
        # Check if letter or directory
        if file_name.endswith('.html'):
            bs = BeautifulSoup(content, 'lxml')
            if bs.title.string == '--IMPORTANT NOTE--':
                file_name = bs.find('a', {'href': re.compile('.*\.(pdf)')})['href']
                content = urlopen(header + file_name).read()

        local_file = open(file_path, 'wb+')
        local_file.write(content)
        local_file.close()


if __name__ == '__main__':
    try:
        scrape_buffett()
    except Exception as e:
        print(e)
