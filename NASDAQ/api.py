import re
import urllib
from bs4 import BeautifulSoup
from alchemyapi import AlchemyAPI


#########################################################################
#   PAGE TEXT EXTRACTION , DATA PROCESSING, SENTIMENT ANALYSIS          #
#########################################################################
def extractArticleText(symbol):
	data = []
	articles = []
	headlines = []
	titles = []
	html = urllib.urlopen('http://www.nasdaq.com/symbol/' + symbol + '/news-headlines')
	soup = BeautifulSoup(html)
	soup = soup.find("div", { "class" : "headlines" })
	
	for b in soup.find_all('small'):
		headline = re.sub(r'[\ \n]{2,}', '', b.text)
		headlines.append(headline.replace("\r\n\t\t", ""))
	#print headlines
	counter = 0
	length = len(headlines)
	for a in soup.find_all('a', href=True):
	    html0 = urllib.urlopen(a['href'])
	    soup0 = BeautifulSoup(html0)
	    titles.append(a.text)
	    for page in soup0.findAll('p'):
	    	#print page.text
		    try:
		    	term = a.text
		    	if(term == ("Motley Fool") or term == ("RTT News") or term == ("Zacks.com")):
		    		pass
		    	else:
		    		if(counter >= length):
		    			break
		    		articles.append([headlines[counter],page.text,sentiment(page.text)])
		    		counter += 1
		    except AttributeError:
		    	pass

	length = min(len(articles), len(titles))
	print length
	for i in xrange(length):
		articles[i].insert(1,titles[i])

	return articles


	#print soup.find("div", {"id": "articleText"}).text
def sentiment(demo_html):
	alchemyapi = AlchemyAPI()
	response = alchemyapi.sentiment('html', demo_html)
	if response['status'] == 'OK':
		if 'score' in response['docSentiment']:
			return (response['docSentiment']['score'])
	else:
		return (0.12)

print extractArticleText("aapl")