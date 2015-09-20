from __future__ import print_function
import re
import urllib
from bs4 import BeautifulSoup
from threading import Thread
from Queue import Queue, Empty
from alchemyapi import AlchemyAPI
import json

concurrent = 20

#########################################################################
#   PAGE TEXT EXTRACTION , DATA PROCESSING, SENTIMENT ANALYSIS          #
#########################################################################
"""
[] Returns text of relevant news headlines
[x] Conducts sentiment analysis on text
[x] returns headlines and dates
[] packages it into a dictionary
"""
alchemyapi = AlchemyAPI()
def extractArticleText(symbol):

    articles = []
    headlines = []
    html = urllib.urlopen('http://www.nasdaq.com/symbol/' + symbol + '/news-headlines')
    soup = BeautifulSoup(html, "html.parser")
    soup = soup.find("div", { "class" : "headlines" })
    
#   for b in soup.find_all('small'):
#       headline = re.sub(r'[\ \n]{2,}', '', b.text)
#       headlines.append(headline.replace("\r\n\t\t", ""))

    # set up threads for parallel work
    # fill the queue with links
    q = Queue()
    p = Queue()
    links = soup.find_all('a', href=True)
    for link in links:
        q.put(link)
    for i in range(concurrent):
        t = Thread(target=parseArticles, args=(q, p, ))
        t.start()
    q.join()
    while p.qsize() > 0:
        articles.append((p.get(),sentiment(p.get())))
    return articles

def parseArticles(q, p):
    while True:
        try:
            a = q.get(False)
            html0 = urllib.urlopen(a['href'])
            soup0 = BeautifulSoup(html0, "html.parser")
            try:
                term = a.text
                if(term == ("Motley Fool") or term == ("RTT News") or term == ("Zacks.com")):
                    pass
                else:
                    p.put(a.text)
            except AttributeError:
                pass
            q.task_done()
        except Empty:
            return

def sentiment(demo_html):
    response = alchemyapi.sentiment('html', demo_html)
    if response['status'] == 'OK':
        if 'score' in response['docSentiment']:
            return (response['docSentiment']['score'])
    else:
        return (0.12)




extractArticleText("Hi my name is bob and Im very sad")

    #print soup.find("div", {"id": "articleText"}).text
















