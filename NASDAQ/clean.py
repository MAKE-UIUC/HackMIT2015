import re
import urllib
from bs4 import BeautifulSoup


#########################################################################
#   PAGE TEXT EXTRACTION , DATA PROCESSING, SENTIMENT ANALYSIS          #
#########################################################################
"""
[] Returns text of relevant news headlines
[x] Conducts sentiment analysis on text
[x] returns headlines and dates
[] packages it into a dictionary
"""
def extractArticleText(symbol):
	articles = []
	headlines = []
	html = urllib.urlopen('http://www.nasdaq.com/symbol/' + symbol + '/news-headlines')
	soup = BeautifulSoup(html)
	soup = soup.find("div", { "class" : "headlines" })
	
#	for b in soup.find_all('small'):
#		headline = re.sub(r'[\ \n]{2,}', '', b.text)
#		headlines.append(headline.replace("\r\n\t\t", ""))
	for a in soup.find_all('a', href=True):
	    html0 = urllib.urlopen(a['href'])
	    soup0 = BeautifulSoup(html0)
	    try:
	    	term = a.text
	    	if(term == ("Motley Fool") or term == ("RTT News") or term == ("Zacks.com")):
	    		pass
	    	else:
	    		articles.append(a.text)
	    	for page in soup0.findAll('p'):
	    		pass#print soup0.find("div", {"id": "articleText"}).text
	    except AttributeError:
	    	pass
	return articles


	#print soup.find("div", {"id": "articleText"}).text

#########################################################################
#####         NEWS HEADLINES EXTRACTION                             #####
#########################################################################




#########################################################################
#####         TF-IDF                                                #####
#########################################################################

#########################################################################
#####         SUMMARIZATION                                         #####
#########################################################################

#########################################################################
#####         TESTING                                               #####
#########################################################################
print extractArticleText("aapl")















