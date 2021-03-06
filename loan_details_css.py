## This file uses file in master branch, edit3.css to overwite 
## a given Kiva loan page to output an html with only the information 
## required for this research. The package beautiful soup is used to 
## draw out the html code, while the css file makes layout changes as 
## well as manipulates information display.

import urllib.request
import requests
from bs4 import BeautifulSoup
import os
import shutil

n = "1313449"
URL = "https://www.kiva.org/lend/" + n
count = 0;

count = count + 1;
req_website = urllib.request.Request(URL, headers={'User-Agent': "Magic Browser"})
website = urllib.request.urlopen(req_website)
soup = BeautifulSoup(website, 'html.parser')
linktag = soup.new_tag('link')
linktag.attrs['rel'] = 'stylesheet'
linktag.attrs['type'] = 'text/css'
linktag.attrs['href'] = 'edit3.css'
soup.head.append(linktag)
filename = n + ".html"
Html_file = open(filename, "w")
Html_file.write(str(soup))
Html_file.close()
