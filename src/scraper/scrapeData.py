'''
Created on Jan 7, 2019

@author: mark
'''
from bs4 import BeautifulSoup
import requests
import os
import csv
import urllib2
import time

# List of item names to search on eBay
name_list = ["Near East Antiquities"]

objects=[]
prices=[]
figures=[]
figuresKeep=[]

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
            info=n.get_text(separator=u" ")
            objects.append(info)
            
        # Scrapes the first listed item's price
        price = soup.find_all("span", {"class": "s-item__price"})
        
        for p in price:
            pr=p.get_text(separator=u" ")
            prices.append(pr)
            
        images=soup.find_all("img",{"class": "s-item__image-img"})
        
        for im in images:
            
            
            src=im['src']
            
            
            if 'images' not in src:
                src=im['data-src']
                
            
            
            figures.append(src)
        
        printImages()

        # Prints the url, listed item name, and the price of the item

def printImages():
    
    for i in range(0,len(figures)):
        f=figures[i]
        
        #get the current time
        
        try:
            download_img = urllib2.urlopen(f)
        
            
        except urllib2.HTTPError:
            continue
        
        
        np=filenameToOutput()
        
        path_to_data=os.path.join(np,'images','.%s.jpg'% i)
        
        
        figuresKeep.append('%s.jpg'% i)
        
        #create the image stream (should go to your current folder this module is in)
        txt = open(path_to_data, "wb")
    
        #write the binary data
    
        txt.write(download_img.read())

        #close the image file
        txt.close()

def printResults():
    fieldnames = ['Object','Price','Figure']
     
    filename=filenameToOutput()
    filename=os.path.join(filename,'output','output.csv')
    
    with open(filename, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()      
        
        i=0
        for o in objects:
            p=prices[i].encode('utf-8').strip()
            f=figuresKeep[i].encode('utf-8').strip()
            
            i+=1
            
            o=o.encode('utf-8').strip()
            writer.writerow({'Object':str(o),'Price':str(p),'Figure':str(f)})

def filenameToOutput():
        '''
        The file name to output the results
        filename-- the filename for the output
        '''  
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        
        return pn
    
''''
The main to launch this module
'''
if __name__ == '__main__':
    ebay_scrape(make_urls(name_list))
    printResults()
