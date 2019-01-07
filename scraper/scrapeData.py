'''
Created on Jan 7, 2019

@author: mark
'''
from bs4 import BeautifulSoup
import requests
import os
import csv

# List of item names to search on eBay
name_list = ["Near East Antiquities"]

objects=[]
prices=[]
figures=[]

# Returns a list of urls that search eBay for an item
def make_urls(names):
    # eBay url that can be modified to search for a specific item on eBay
    url = "https://www.ebay.com/sch/91101/i.html?_from=R40&_nkw="
    # List of urls created
    urls = []

    for name in names:
        # Adds the name of item being searched to the end of the eBay url and appends it to the urls list
        # In order for it to work the spaces need to be replaced with a +
        urls.append(url + name.replace(" ", "+"))

    # Returns the list of completed urls
    return urls


# Scrapes and prints the url, name, and price of the first item result listed on eBay
def ebay_scrape(urls):
    for url in urls:
        # Downloads the eBay page for processing
        res = requests.get(url)
        # Raises an exception error if there's an error downloading the website
        res.raise_for_status()
        # Creates a BeautifulSoup object for HTML parsing
        soup = BeautifulSoup(res.text, 'html.parser')
        # Scrapes the first listed item's name
        name = soup.find_all("h3", {"class": "s-item__title"})
        # .get_text(separator=u" ")
        for n in name:
            objects.append(n)
        # Scrapes the first listed item's price
        price = soup.find_all("span", {"class": "s-item__price"})
        
        for p in price:
            prices.append(p)

        # Prints the url, listed item name, and the price of the item

def printResults():
    fieldnames = ['Object','Price','Figure']
     
    filename=filenameToOutput()
    
    with open(filename, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()      
        
        i=0
        for o in objects:
            p=prices[i]
            f=figures[i]
            
            i+=1
            
            writer.writerow({'Object':str(o),'Price':str(p),'Figure':str(f)})

def filenameToOutput():
        '''
        The file name to output the results
        filename-- the filename for the output
        '''  
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        filename=os.path.join(pn,'output','termFrequencies.csv')
        
        return filename
    
''''
The main to launch this module
'''
if __name__ == '__main__':
    ebay_scrape(make_urls(name_list))
