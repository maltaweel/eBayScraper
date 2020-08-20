'''
Module used to scrape data from sold eBay information on antiquities and cultural objects.

Created on Jan 7, 2019

@author: 
'''
from bs4 import BeautifulSoup
import requests
import os
import csv
import datetime
import urllib3

# List of item names to search on eBay based on what is present on the eBay site.
name_list = ["Near East Antiquities",'Egyptian Antiquities', 'Antiquities of The Americas',
             'Byzantine Antiquities','Celtic Antiquities','Far Eastern Antiquities','Greek Antiquities',
             'Holy Land Antiquities','Islamic Antiquities','Neolithic & Paleolithic Antiquities',
             'Roman Antiquities','South Italian Antiquities', 'Viking Antiquities', 'Other Antiquities']

#tracking numbers
ii=0
tt=0

#lists and dictionaries for data to scrape and keep for outputting.

#object information
objects=[]

sell={}

#price data
prices=[]

#figures (images)
figures={}
figuresKeep={}

#link data
links={}

#location of the sale data
location={}

'''
Method that returns urls to search and scrape data.
@param names- the names of eBay sites to search
@return urls to search
'''
def make_urls(names):
#    eBay url that can be modified to search for a specific item on eBay
#    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1312.R1.TR11.TRC2.A0.H0.XIp.TRS1&_nkw="
#    url='https://www.ebay.com/sch/i.html?_from=R40&_nkw='
#    url='https://www.ebay.com/sch/37907/i.html?_sop=13&_sadis=15&LH_Auction=1&LH_Complete=1&LH_Sold=1&_stpos=90278-4805&_from=R40&_nkw=%27'
    
    #the main url to search and then add additional names to scrape within eBay
    url='https://www.ebay.com/sch/37903/i.html?_sop=13&_sadis=15&LH_Auction=1&LH_Complete=1&LH_Sold=1&_stpos=90278-4805&_from=R40&_nkw=%27+'
    
    # List of urls created
    urls = {}

    for name in names:
        # Adds the name of item being searched to the end of the eBay url and appends it to the urls list
        # In order for it to work the spaces need to be replaced with a +
        urls[name]=url + name.replace(" ", "+")
        

    # Returns the list of completed urls
    return urls

'''
Method to scrape data and print the individual object urls, location of objects sold, description of objects, 
and price of the item result listed on eBay.

@param url- the url to scrape
@param tt- the iteration number of each set of urls to scrape
'''
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
        nnt=soup.find_all("span", {"class":'s-item__ended-date s-item__endedDate'})

        # .get_text(separator=u" ")
        
        for n in name:
            info=n.get_text(separator=u" ")
            tn=nnt[iit]
            date=tn.get_text(separator=u" ")
            date1=date.split(" ")[0]
            date=date1.replace("-"," ")+", "+str(datetime.datetime.now().year)
            info=date+ " "+info     
            
            objects.append(info)
            localNames.append(info)
            tt+=1
            iit+=1
            # Scrapes the first listed item's price
            
        #scrape the price
        price = soup.find_all("span", {"class": "s-item__price"})
                   
        for p in price:
            pr=p.get_text(separator=u" ")
            prices.append(pr)
            
          
        imags=soup.find_all("a",{"class": "s-item__link"})
        
        soup.decompose()
        
        
        iit=0
        #this gets data from the html
        for im in imags:
            name=localNames[iit]
            
            href=im['href']
            res2 = requests.get(href)
            soup2 = BeautifulSoup(res2.text, 'html.parser')
            
            location1 = soup2.find_all("div", {"class": "u-flL"})
            location2 = soup2.find_all("div",{"class": "sh-loc"})
            seller=soup2.find_all("span",{'class':'mbg-nw'})
            
#            print(href)
            links[name]=href
            
            #location data
            tr=False
            for lc2 in location2:
                prr=lc2.get_text(separator=u" ").split("location: ")[1]
                location[name]=prr
                tr=True
            
            loc=False
            if tr is False:
                for lc3 in location1:
                    text=lc3.get_text(separator=u" ")
                    if "Item location" in text:
                        loc=True
                        continue
                    if loc is True:
                        prr=lc3.get_text(separator=u" ")
                        location[name]=prr
                        break
                    
            for se in seller:
                for cc in se.contents:
                    ssT=str(cc)
                    sell[name]=ssT
                    sellR=ssT
            
            iit+=1
            

#        break
'''
Method to print the images from a given description page,
Method is not currently used.
@param ii- the image number to print
'''
def printImages(ii):
    
   
    for n in figures.keys():
#        print(n)
        
        f=figures[n]
        
#        print(f)
        #get the current time
        
        try:
            download_img = requests.get(f)
           
        except urllib3.exceptions.HTTPError:
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

'''
Method to output the eBay data scrapped.
@param name- the name of the output file to put the data to. The output folder has the eBay data retrieved.
'''
def printResults(name):
    fieldnames = ['Object','Price','Location','Seller','Link']
     
    filename=filenameToOutput()
    filename=os.path.join(filename,'output',name+'.csv')
    
    #here we open the results which will the name of cultures scraped from eBay
    with open(filename, 'w') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()      
        
        i=0
        
        
        for o in objects:
            p=prices[i].encode('utf-8').strip()
            
            try:
                no=o.split("2019 ")[1]
            except:
                try:
                    no=o.split("2018 ")[1]
                except:
                    continue
            
            if no in figuresKeep.keys():
                f=figuresKeep[no].encode('utf-8').strip()
            else:
                f=""
            
            i+=1
            
            
            l=""
            liks=''
            sel=''
            
            try:
                l=location[o].encode('utf8').strip()
            except:
                l=""
            
            try:
                sel=sell[o].encode('utf8').strip()
            except:
                sel=""
                
            try:
                liks=links[o].encode('utf8').strip()
            except:
                liks=""
            
            o=o.encode('utf-8').strip()  
            writer.writerow({'Object':str(o),'Price':str(p),'Location':str(l),'Seller':str(sel),'Link':str(liks)})
    
    #clear the containers
    del objects[:]
    del prices[:]
    sell.clear()
    location.clear()
    links.clear()
    figures.clear()
    figuresKeep.clear()

'''
The file output path for printing results (to the src level of this project)
@return rn- the output file path to use to the src level
''' 
def filenameToOutput():
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        
        return pn

def runModule():
    urls=make_urls(name_list)
    
    
    for name in urls.keys():
       
        
        tt=0
        
        #url used
        url=urls[name]
        
        #scrape here
        ebay_scrape(url,tt)
#       printImages(ii)

        #print results
        printResults(name)
        
#        break
 
    print('Finished')

if __name__ == '__main__':
    runModule()