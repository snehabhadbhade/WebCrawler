import urllib
from urlparse import urlparse
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
from urlparse import urljoin
import sys
import time

class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]

    def getLinks(self, url):
        #print url
        self.links = []
        self.baseUrl = url
        try :
	    time.sleep(2)
            response = urllib.urlopen(url)
            html = response.read()
            self.feed(html)
        except:
            self.links = []
        #print self.links
        return self.links

'''
def parse_link(url):
    links = []
    parsed = urlparse(url)
    base_url = parsed.scheme + '://' + parsed.netloc
    response = urllib.urlopen(url)
    html = response.read()
    #htmlString = htmlBytes.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.findAll('a'):
        if link.has_attr("href"):
            url_link = link.get("href")
            parsed = urlparse(url_link)
            if parsed.netloc == '':
                if parsed.path:
                    if parsed.path[0] == '/':
                        url_link = base_url +  url_link
                    else:
                        url_link = url + '/' + url_link
                else:
                        url_link = url + url_link
            links.append(url_link)

    return links
'''


seed_url = sys.argv[1]
dest_file = sys.argv[2]

parsed = urlparse(seed_url)

robots_url = seed_url.replace(parsed.path,"/robots.txt")
base_url = seed_url.replace(parsed.path,"")

urls_disallowed = []
response = urllib.urlopen(robots_url)

for line in response:
    if "Disallow: " in line:
        line = line.strip("\n")
        line = line.replace("Disallow: ", "")
        url = base_url + line
        urls_disallowed.append(url)

pagesToVisit = [seed_url]
numberVisited = 0
linksVisited = []
linksFound = []

while pagesToVisit != []:
        numberVisited = numberVisited + 1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        parser = LinkParser()
        links = parser.getLinks(url)
        linksVisited.append(url)
        for link in links:
            if link not in linksFound:
                linksFound.append(link)
            if link not in urls_disallowed and seed_url in link and link not in linksVisited:
                parsed = urlparse(link)
                if parsed.fragment:
                    anchor = "#"+ parsed.fragment
                    url_parsed = link.replace(anchor,"")
                    if url_parsed not in linksVisited and url_parsed not in pagesToVisit:
                        pagesToVisit.append(url_parsed)
                else:
                    if link not in linksVisited and link not in pagesToVisit:
                        pagesToVisit.append(link)

        #print linksFound



with open(dest_file, "w") as f:
    for url in linksFound:
        output = str(url) + "\n"
        f.write(output)

f.close()




