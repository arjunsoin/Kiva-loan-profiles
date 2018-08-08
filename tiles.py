import requests
import bs4
import imgkit
import pdfcrowd
import subprocess
import random
import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import requests
import os
import shutil
from GrabzIt import GrabzItClient
from GrabzIt import GrabzItImageOptions
from PIL import Image

url_list = [int(x) for x in input("Enter space-separated urls: ").split()]

for n in url_list:

	URL = "https://www.kiva.org/lend?queryString=" + str(n) + "&status=all"

	chromedriver = "/Users/arjunsoin/Desktop/chromedriver"
	browser = webdriver.Chrome(chromedriver)
	browser.get(URL)
	html = browser.page_source
	soup = BeautifulSoup(html,"lxml")

	s = 91929 ## replace s with url in for loop 
	fl = '%s.html' % s ## replace with url 
	di = os.getcwd()
	final = di + "/" + fl

	with open(final, "w") as file:
		file.write(str(soup))

	options = GrabzItImageOptions.GrabzItImageOptions()
	options.width = -1
	options.height = -1
	options.browserHeight = -1

	grabzIt = GrabzItClient.GrabzItClient("NmViOGJhNjk0YjRiNGU4OTlhNDFiNjk2MDliOTY2MDM=", "KzA/ID8LVz8/P3F+X2M/Pz8/RT9VPz8mPz8/Pz8/Pyc=")
	grabzIt.FileToImage(final, options) 
	filepath = di + '/result.jpg'
	grabzIt.SaveTo(filepath) 

	im = Image.open(filepath)
	outfile = str(n) + "_tile.jpg"
	region=im.crop((40, 350, 330, 651))
	region.save(outfile, "JPEG")
