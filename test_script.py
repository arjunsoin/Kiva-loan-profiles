import requests
import bs4
import pdfcrowd
import subprocess
import sys
import os
from selenium import webdriver
from bs4 import BeautifulSoup

## Get the html code of webpage and convert into 'Beautiful Soup' element for parsing
def access_source_code(url):
	chromedriver = "/Users/arjunsoin/Desktop/chromedriver"
	browser = webdriver.Chrome(chromedriver)
	webpage = "https://www.kiva.org/lend/" + str(url)
	browser.get(webpage)
	html = browser.page_source
	soup = BeautifulSoup(html,"lxml")
	return soup 

## Function removes extra line-breaks, header and footer of page 
def clean_up(page):
	question_action = page.find('div', attrs={'class': 'full-width-green-bar'})
	question_action.clear()

	for x in page.findAll("div","xbLegacyNav"):
		x.decompose()

	line = page.find('section', {'class': 'more-loan-info'})
	if page.find('section', {'class': 'more-loan-info'}) is not None: 
	    line = page.find('section', {'class': 'more-loan-info'}).find_previous_sibling('hr')
	    if line is not None:
	        line.decompose()

	line2 = page.find('section', {'class': 'lenders-teams'})
	if page.find('section', {'class': 'lenders-teams'}) is not None: 
	    line2 = page.find('section', {'class': 'lenders-teams'}).find_previous_sibling('hr')
	    if line2 is not None:
	        line2.decompose()
	    
	line3 = page.find('section', {'class': 'country-info'})
	if page.find('section', {'class': 'country-info'}) is not None: 
	    line3 = page.find('section', {'class': 'country-info'}).find_previous_sibling('hr')
	    if line3 is not None:
	        line3.decompose()
	    
	line4 = page.find('section', {'class': 'loan-tags'})
	if page.find('section', {'class': 'loan-tags'}) is not None: 
	    line4 = page.find('section', {'class': 'loan-tags'}).find_previous_sibling('hr')
	    if line4 is not None:
	        line4.decompose()


def capture_top_right(page):
	lender_count = page.find('a', attrs={'class': 'lender-count black-underlined'})
	lender_count.clear()

	status = page.find('h2', attrs={'class': 'green-bolded inline'})
	status.clear()

	lender_action = page.find('div', attrs={'class': 'show-for-large-up lend-action'})
	lender_action.clear()

	raised_info = page.find('div', attrs={'class': 'raised-info row'})
	raised_info.clear()

	return

def capture_bottom_right(page):
	right_info = page.find('div', attrs={'class': 'right-content columns'})
	right_info.clear()

	details = page.find('section', attrs={'class': 'loan-details'})
	details.clear()

	for e in page.findAll("div","stat"):
		e.clear()

	return

def extend_text(page):
	div_page_content = page.find("div", { "class" : "borrower-profile-pieces" })
	button_active = page.new_tag('style', type='text/css')
	div_page_content.attrs['style'] = 'background: #FFF'

	div_page_content = page.find("div", { "class" : "right-content columns" })
	button_active = page.new_tag('style', type='text/css')
	div_page_content.attrs['style'] = 'background-color: white'

	search = page.find("div", { "class" : "left-content columns" })
	search['class'] = 'columns'

def capture_bottom_left(page):

	x = page.find('div', {'aria-controls': 'ac-more-loan-info-body'})
	if x is not None:
		temp = x.find('h2')
		if temp is not None:
			temp.clear()

	tags_text = page.find('div', {'class': 'ac-title-text'})
	if tags_text is not None:
	    tags_text.clear()

	lenders = page.find('section', attrs={'class': 'lenders-teams'})
	lenders.clear()

	country_info = page.find('section', attrs={'class': 'country-info'})
	country_info.clear()

	return


def generate_output(url,page):
	s = str(url)
	fl = '%s.html' % str(url)  
	di = os.getcwd()
	final = os.path.join(di,fl)  
	
	with open(final, "w") as file:
		file.write(str(page))
    
    ## Use pdfcrowd API to convert html to png output 
	client = pdfcrowd.HtmlToImageClient('arjunsoin', '857e0066edce5f22fc537177d3de04a3')
	client.setOutputFormat('png')
	client = client.setScreenshotHeight(1250)
	client.convertFileToFile(final, '%s.png' % str(url))
	return


## Ask for user-input in the form of space-separated url numbers
url_list = [int(x) for x in input("Enter space-separated urls: ").split()]

## Run and generate output for each entered user 'url'
for url in url_list:
	webpage = access_source_code(url)
	clean_up(webpage)
	capture_top_right(webpage)
	capture_bottom_right(webpage)
	extend_text(webpage)
	capture_bottom_left(webpage)
	generate_output(url,webpage)

