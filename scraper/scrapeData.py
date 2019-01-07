'''
Created on Jan 7, 2019

@author: mark
'''
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib
from lxml import etree

try:
    print("running with lxml.etree")
except ImportError:
    print("It appears you either have an outdated Python version, or you haven't installed lxml. See README.md file for details on how to address this error.")

# start Firefox instance
driver = webdriver.Chrome()

# change this value to alter the number of tries before a url request times out
num_requests = 10

found = False

# change this value to alter the default url to scrape
url = "http://www.ebay.co.uk/sch/Near-Eastern"

while(num_requests > 0):
    try:
        driver.get(url)
        print(driver.title)
        num_requests = 0
        found = True
    except:
        num_requests -= 1
        print("warning: a parsing error occured -- " + num_requests + " requests left")
        pass

if(found == True):
    try:
        # change this value if you want to do something
        # other than return terms based on searches
        inputElement = driver.find_element_by_id("gh-ac")
        # change term to search for something other than shoes
        inputElement.send_keys("")
        
        # enter search data
        inputElement.submit()
    except:
        print("this element does not exist")
else:
    print("no website found at URL")

