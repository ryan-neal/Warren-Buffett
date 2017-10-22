import re
import os
import sys

from urllib.request import urlopen
from bs4 import BeautifulSoup


SAVE_DIR = os.getcwd() + '/data/raw/'

def scrape_buffett():
	header = 'http://www.berkshirehathaway.com/letters/'
	page = urlopen('http://www.berkshirehathaway.com/letters/letters.html')
	soup = BeautifulSoup(page.read(), 'lxml')	
	tags = soup.findAll('a', {'href' : re.compile('.*\.(html)|(pdf)')})
	files = map(lambda tag: tag['href'], tags)
	for file in files:
		local_file = open(SAVE_DIR+file, 'wb')
		response = urlopen(header + file)
		local_file.write(response.read())
		local_file.close()

if __name__ == '__main__':
	if sys.argv[1] == 'buffett':
		scrape_buffett()