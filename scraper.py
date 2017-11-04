import re
import os
import sys

from urllib.request import urlopen
from bs4 import BeautifulSoup

SAVE_DIRS = {
    'Buffett': os.getcwd().rsplit('Warren-Buffett', 1)[0] + 'Warren-Buffett/data/raw/'
}


def scrape_buffett(save_dir=SAVE_DIRS['Buffett']):
    header = 'http://www.berkshirehathaway.com/letters/'
    page = urlopen('http://www.berkshirehathaway.com/letters/letters.html')
    soup = BeautifulSoup(page.read(), 'lxml')
    tags = soup.findAll('a', {'href': re.compile('.*\.(html)|(pdf)')})

    files = map(lambda tag: tag['href'], tags)
    for file in files:
        content = urlopen(header + file).read()
        # Check if letter or directory
        if file.endswith('.html'):
            bs = BeautifulSoup(content, 'lxml')
            if bs.title.string == '--IMPORTANT NOTE--':
                file = bs.find('a', {'href': re.compile('.*\.(pdf)')})['href']
                content = urlopen(header + file).read()
        local_file = open(save_dir+file, 'wb')
        local_file.write(content)
        local_file.close()


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'buffett':
            scrape_buffett()
    except Exception as e:
        print(e)
        pass
