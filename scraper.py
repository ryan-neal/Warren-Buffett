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
	tags = soup.findAll('a', {'href' : re.compile('.*\.(html)|(pdf)')})
	files = map(lambda tag: tag['href'], tags)
	for file in files:
		local_file = open(save_dir+file, 'wb')
		response = urlopen(header + file)
		local_file.write(response.read())
		local_file.close()

if __name__ == '__main__':
	try:
		if sys.argv[1] == 'buffett':
			scrape_buffett()
	except:
		pass