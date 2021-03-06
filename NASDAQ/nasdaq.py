import urllib
import urllib2
import xml.etree.cElementTree as ElementTree
import re
from pprint import pprint
import datetime as dt

#Alchemy Keys
CONSUMER_KEY = "blzC40MytkH9HguJYBUcttxxg"
CONSUMER_SECRET = "Mw37mXO7sXUNazbUkUlfsfjSzQCMIXNZXD3wuSmJeQj1tvnm2e"
ACCESS_TOKEN_KEY = "2658435840-MjNaSPPQso4aMFK1C1SgB5S8ISlRSAlQsPLFB74"
ACCESS_TOKEN_SECRET = "iTF4QJcKlu4ZCOJbtbJTTGvO1xHjRSB5JZJCrdTjyJQrB"




class Xml2List(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(Xml2Dict(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(Xml2List(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)

# Returns a dictionary
class Xml2Dict(dict):
    '''
    Example usage:

    Given an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = Xml2Dict(root)

    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = Xml2Dict(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = {element[0].tag: Xml2List(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell.
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})


## API Test ##

url = 'http://ws.nasdaqdod.com/v1/NASDAQAnalytics.asmx/GetEndOfDayData'
# Change symbols and date range (not more that 30 days at a time)
values = {'_Token' : '92E9B809A616440490396CB7601E0A34',
          'Symbols' : 'GOOG',#'GOOG,AAPL,QQQ',
          'StartDate' : '9/14/2015',
          'EndDate' : '9/18/2015',
          'MarketCenters' : '' }

# Build HTTP request
request_parameters = urllib.urlencode(values)
req = urllib2.Request(url, request_parameters)

# Submit request
try:
    response = urllib2.urlopen(req)
    
except urllib2.HTTPError as e:
    print e.code
    print e.read()

# Read response
the_page = response.read()

# Remove annoying namespace prefix
the_page = re.sub(' xmlns="[^"]+"', '', the_page, count=1)

# Parse page XML from string
root = ElementTree.XML(the_page)

# Cast ElementTree to list of dictionaries
data = Xml2List(root)

# Package the data into a useful format
closing_prices = []

if data[0]["Outcome"] == 'RequestError' and "Prices" not in data[0]:
    print "Web Request Error :(  Make sure that you arent pulling more that one month of data. "
    print the_page


for i in data:
    closing_prices.append({'Symbol':i['Symbol'],'Dates':[],'Prices':[],'Volume':[], 'PercentChange':[]})
    
    for price in i['Prices']['EndOfDayPrice']:

        try:
            closing_prices[-1]['Dates'].append(price['Date'])
            closing_prices[-1]['Volume'].append(price['Volume'])
            closing_prices[-1]['Prices'].append(float(price['Close']))
            
            ## Normalize prices to show percent change from start of time range
            closing_prices[-1]['PercentChange'].append(100*(closing_prices[-1]['Prices'][-1]-
                closing_prices[-1]['Prices'][0])/
                closing_prices[-1]['Prices'][0])

        except(Exception) as e:
            print "Skipping non-trading date."

# Examine new dictionary
pprint(closing_prices)



