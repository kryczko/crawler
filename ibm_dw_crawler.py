#!/usr/bin/env python

import urllib2, HTMLParser
import lxml.html as lhtml
from alchemyapi import AlchemyAPI
import pickle, sys

from selenium import webdriver

browser = webdriver.Firefox()
#browser.implicitly_wait(60)

class Worker():
	def __init__(self):
		self.main_url = ''
		self.worker_id = -1
		self.urls = []
		self.webpage_keywords = []
		self.webpage_sentiments = []
		self.webpage_titles = []
		self.webpage_bodies = []

	def get_links(self):
		browser.get(self.main_url)
		html_string = browser.page_source
		parsed_html = lhtml.fromstring(html_string)
		links = parsed_html.findall('.//tr/td/h4/a')
		for link in links:
			unstripped = link.get('href')
			stripped = unstripped.lstrip('\n')
			self.urls.append(stripped)


class Status:
	def intro(self):
		print ("Welcome, this web crawler is designed to look at IBM's developerworks webpage and summarize the problems.")
		print ("\nThe web crawling is about to begin.")

def init_workers(starting_page, number_of_pages, url):
	workers = []
	for i in range(starting_page, starting_page + number_of_pages):
		current_url = url + str(i)
		worker = Worker()
		worker.main_url = current_url
		worker.worker_id = i
		worker.get_links()
		workers.append(worker)
		print ("Worker %i has found %i forums." % (worker.worker_id, len(worker.urls)))
	return workers

def call_alchemy(alchemyapi, workers):
	worker_count = 0
	for worker in workers:
		url_count = 0
		for url in worker.urls:
			keywords = alchemyapi.keywords('url', url)
			sentiment = alchemyapi.sentiment('url', url)
			title = alchemyapi.title('url', url)
			text = alchemyapi.text('url', url)
			worker.webpage_keywords.append(keywords)
			worker.webpage_sentiments.append(sentiment)
			worker.webpage_titles.append(title)
			worker.webpage_bodies.append(text)
			print ('Called the AlchemyAPI for url: %i, worker: %i | Number of API calls: %i' % (url_count, worker_count, (worker_count + 1) * (url_count + 1) * 4))
			url_count += 1
		worker_count += 1

		#assert(response['status'] == 'OK')

def serialize(workers):
	output = str(sys.argv[3])
	f = open(output, 'w')
	pickle.dump(workers, f)
	f.close()

def arg_check():
	if len(sys.argv) == 1:
		print ("ERROR: Invalid Syntax for command line arguments. Run: ./ibm_dw_crawler.py --help")
		exit(-1)
	elif sys.argv[1] == '--help':
		print ("Syntax is ./ibm_dw_crawler.py [starting page] [number of pages] [serialized file name]")
		print ("\nExample: ./ibm_dw_crawler.py 0 5 data_page_0-5.dat")
		print( "\nThe above example will start at the forum page 0 and stop at the forum page 4 outputting all of the data to the serialized file \'data_page_0-5.dat\'.")
		print ("\nOnce finished, the data can be accessed again with python using the pickle library.")
		exit(-1)

def main():
	arg_check()

	status = Status()
	status.intro()
	alchemyapi = AlchemyAPI()
	
	starting_page = int(sys.argv[1])
	number_of_pages = int(sys.argv[2])


	print ("Starting with forum page: %i" % starting_page)
	print ("Ending with page: %i" % (starting_page + number_of_pages - 1))
	print ("Total number of AlchemyAPI calls projected: %i" % (number_of_pages * 25 * 4))
	print ("Reminder: The number of AlchemyAPI calls is 4 per page.")
	
	# starting url is the developer works webpage
	main_url = "https://www.ibm.com/developerworks/community/forums/html/forum?id=11111111-0000-0000-0000-000000000842#topicsPg="

	workers = init_workers(starting_page, number_of_pages, main_url)
	call_alchemy(alchemyapi, workers)
	serialize(workers)
if __name__ == "__main__":
	main()