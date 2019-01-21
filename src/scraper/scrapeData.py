'''
Created on Jan 7, 2019

@author: mark
'''
from bs4 import BeautifulSoup
import requests
import os
import csv
import urllib2

# List of item names to search on eBay
name_list = ["Near East Antiquities",'Egyptian Antiquities', 'Antiquities of The Americas',
             'Byzantine Antiquities','Celtic Antiquities','Far Eastern Antiquities','Greek Antiquities',
             'Holy Land Antiquities','Islamic Antiquities','Neolithic & Paleolithic Antiquities',
             'Roman Antiquities','South Italian Antiquities', 'Viking Antiquities', 'Other Antiquities']
#name_list=['Byzantine Antiquities']

ii=0
tt=0


# Returns a list of urls that search eBay for an item
def make_urls(names):
  # eBay url that can be modified to search for a specific item on eBay
#    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1312.R1.TR11.TRC2.A0.H0.XIp.TRS1&_nkw="
#    url='https://www.ebay.com/sch/i.html?_from=R40&_nkw='
#    url='https://www.ebay.com/sch/37907/i.html?_sop=13&_sadis=15&LH_Auction=1&LH_Complete=1&LH_Sold=1&_stpos=90278-4805&_from=R40&_nkw=%27'
    url='https://www.ebay.com/sch/37903/i.html?_sop=13&_sadis=15&LH_Auction=1&LH_Complete=1&LH_Sold=1&_stpos=90278-4805&_from=R40&_nkw=%27+'
    # List of urls created
    urls = {}

    for name in names:
        # Adds the name of item being searched to the end of the eBay url and appends it to the urls list
        # In order for it to work the spaces need to be replaced with a +
        urls[name]=url + name.replace(" ", "+")
        

    # Returns the list of completed urls
    return urls


# Scrapes and prints the url, name, and price of the first item result listed on eBay
def ebay_scrape(url,tt):
    
    # Downloads the eBay page for processing
    originalUrl=url
           
    nn=1
    
    run=True
    
    while(run):
        iit=0   
        localNames=[]
#            if nn==5:
#                break
            
        url=originalUrl+'+%27&_pgn='+str(nn)
            
        print(url)
        res = requests.get(url)
        
        
        # Raises an exception error if there's an error downloading the website
        res.raise_for_status()
            
           
        # Creates a BeautifulSoup object for HTML parsing
        soup = BeautifulSoup(res.text, 'html.parser')
            
        num=soup.find('h1',{"class":'srp-controls__count-heading'})
        number=num.get_text(separator=u" ").split(" results")[0]
        number=number.replace(',','')
            
#       print(int(number))
            
        if int(number)==0:
            run=False
            break
        else:
            nn+=1
        
        if tt>int(number):
                run=False
                break
        # Scrapes the first listed item's name
        name = soup.find_all("h3", {"class": "s-item__title"})

        # .get_text(separator=u" ")
        
        for n in name:
            info=n.get_text(separator=u" ")
#          
            objects.append(info)
            localNames.append(info)
            tt+=1
            iit+=1
                
            # Scrapes the first listed item's price
       
        price = soup.find_all("span", {"class": "s-item__price"})
                
        for p in price:
            pr=p.get_text(separator=u" ")
            prices.append(pr)
            
          
        imags=soup.find_all("a",{"class": "s-item__link"})
        
        soup.decompose()
        
        
        iit=0
        for im in imags:
            name=localNames[iit]
            
            href=im['href']
            res2 = requests.get(href)
            soup2 = BeautifulSoup(res2.text, 'html.parser')
            
            location1 = soup2.find_all("div", {"class": "u-flL"})
            location2 = soup2.find_all("div",{"class": "sh-loc"})
            
#            print(href)
            links[name]=href
            
            tr=False
            for lc2 in location2:
                prr=lc2.get_text(separator=u" ").split("location: ")[1]
                location[name]=prr
                tr=True
#                print(prr)
            
            loc=False
            if tr is False:
                for lc3 in location1:
                    text=lc3.get_text(separator=u" ")
                    if "location" in text:
                        loc=True
                        continue
                    if loc is True:
                        prr=lc3.get_text(separator=u" ")
#                        print(prr)
                        location[name]=prr
                        break
            
            iit+=1
#            src=im['src']
#            alt=im['alt']
            
#            if 'images' not in src:
                    
                    
 #               try:
 #                   src=im['data-src']
 #               except:
 #                   continue
                    
#            figures[alt]=src
            
        
##        print(tt)
        
        # Prints the url, listed item name, and the price of the item

def printImages(ii):
    
   
    for n in figures.keys():
#        print(n)
        
        f=figures[n]
        
#        print(f)
        #get the current time
        
        try:
            download_img = urllib2.urlopen(f)
           
        except urllib2.HTTPError:
            continue
        
        
        np=filenameToOutput()
        
        fileJ='%s.jpg'% ii
        path_to_data=os.path.join(np,'images',fileJ)
        
        
        figuresKeep[n]=fileJ
        
        #create the image stream (should go to your current folder this module is in)
        txt = open(path_to_data, "wb")
    
        #write the binary data
    
        txt.write(download_img.read())

        #close the image file
        txt.close()
        ii+=1

def printResults(name):
    fieldnames = ['Object','Price','Location','Link']
     
    filename=filenameToOutput()
    filename=os.path.join(filename,'output',name+'.csv')
    
    with open(filename, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()      
        
        i=0
        
        
        for o in objects:
            p=prices[i].encode('utf-8').strip()
            
            try:
                no=o.split("2019 ")[1]
            except:
                no=o.split("2018 ")[1]
            
            if no in figuresKeep.keys():
                f=figuresKeep[no].encode('utf-8').strip()
            else:
                f=""
            
            i+=1
            
            o=o.encode('utf-8').strip()
            
            l=""
            liks=''
            
            try:
                l=location[o].encode('utf8').strip()
            except:
                l=""
            
            try:
                liks=links[o].encode('utf8').strip()
            except:
                liks=""
                
            writer.writerow({'Object':str(o),'Price':str(p),'Location':str(l),'Link':str(liks)})
    
    objects[:]
    prices[:]
    figures.clear()
    figuresKeep.clear()
    links.clear()
    location.clear()

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
    urls=make_urls(name_list)
    
    ii=0
    for name in urls.keys():
        objects=[]
        prices=[]
        figures={}
        figuresKeep={}
        links={}
        location={}
        
        tt=0
        url=urls[name]
        ebay_scrape(url,tt)
#       printImages(ii)
        printResults(name)
        
    print('Finished')
