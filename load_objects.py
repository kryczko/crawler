#!/usr/bin/env python

import pickle, os
from ibm_dw_crawler import Worker
import numpy as np


def sentiment_distro():
	n_bins = 100
	counts = np.zeros(n_bins + 1)
	array_of_data = []
	for filename in os.listdir(os.getcwd() + '/datafiles'):
	    rf = 'datafiles/' + filename
	    f = open(rf, 'r')
	    workers = pickle.load(f)
	    i = 0
	    for worker in workers:
	    	for sentiment in worker.webpage_sentiments:
	    		array_of_data.append(float(sentiment['docSentiment']['score']))
	    		print i, float(sentiment['docSentiment']['score'])
	    		i += 1
	    f.close()
	

	nparray_of_data = np.array(array_of_data)
	fake_data = nparray_of_data + abs(min(nparray_of_data))
	domain = max(fake_data) - min(fake_data)
	ds = domain / n_bins

	for val in fake_data:
		bin_num = val / domain
		counts[int(bin_num * 100)] += 1
	
	fo = open('output/sentiment_distro.dat', 'w')
	fo.write('# sentiment\tcount\n\n')
	for i in range(len(counts)):
		fo.write('%f\t%i\n' % (i*ds - abs(min(nparray_of_data)), counts[i]))
		fo.write('%f\t%i\n' % ((i+1)*ds - abs(min(nparray_of_data)), counts[i]))
	fo.close()


def main():
	sentiment_distro()
if __name__ == "__main__":
	main()