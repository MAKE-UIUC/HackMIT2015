import re
import urllib
from bs4 import BeautifulSoup


#########################################################################
#####         PAGE TEXT EXTRACTION                                  #####
#########################################################################
"""
Returns text of relevant news headlines
"""
def extractText(symbol):
	html = urllib.urlopen('http://www.nasdaq.com/symbol/' + symbol + '/news-headlines')
	soup = BeautifulSoup(html)
	soup = soup.find("div", { "class" : "headlines" })
	for a in soup.find_all('a', href=True):
	    html0 = urllib.urlopen(a['href'])
	    soup0 = BeautifulSoup(html0)
	    try:
	    	#print a['href']
	    	for page in soup0.findAll('p'):
	    		pass
	    	#print soup0.find("div", {"id": "articleText"}).text
	    except AttributeError:
	    	pass
	#print soup.find("div", {"id": "articleText"}).text

#########################################################################
#####         NEWS TEXT DATA PROCESSING                             #####
#########################################################################

#########################################################################
#####         NEWS TEXT SENTIMENT ANALYSIS                          #####
#########################################################################

#########################################################################
#####         NEWS HEADLINES EXTRACTION                             #####
#########################################################################

#########################################################################
#####         TF-IDF                                                #####
#########################################################################

















