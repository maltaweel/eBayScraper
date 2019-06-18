'''
Created on Jun 14, 2019

@author: mark
'''

from bs4 import BeautifulSoup
import os
import csv
import requests
import scrapeData as sD

url='https://www.ebay.co.uk/sch/Antiquities/37903/i.html?_udlo=&_udhi=&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=SL11AE&_sop=12&_dmd=1&_nkw=antiquities&_pgn='
prt2='&_skc=50&rt=nc'
name_list = ["British",'Chinese', 'Roman','Americas','Other Antiquities','Egyptian','Prehistoric',
             'Greek','Near Eastern','Scandinavian','European','Russian']

def make_urls():
  # eBay url that can be modified to search for a specific item on eBay
#    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1312.R1.TR11.TRC2.A0.H0.XIp.TRS1&_nkw="
#    url='https://www.ebay.com/sch/i.html?_from=R40&_nkw='
#    url='https://www.ebay.com/sch/37907/i.html?_sop=13&_sadis=15&LH_Auction=1&LH_Complete=1&LH_Sold=1&_stpos=90278-4805&_from=R40&_nkw=%27'
    
    # List of urls created
    urls = []

    for i in range(1,10000000):
        # Adds the name of item being searched to the end of the eBay url and appends it to the urls list
        # In order for it to work the spaces need to be replaced with a +
        urlFull=url + str(i)+prt2
        run=ebay_scrape(urlFull)
        
        
        

    # Returns the list of completed urls

def ebay_scrape(urlFull):
    
    # Downloads the eBay page for processing
    originalUrl=urlFull
           
    nn=1
    
    run=True
    
    while(run):

        print(originalUrl)
        res = requests.get(originalUrl)
        
        
        # Raises an exception error if there's an error downloading the website
        try:
            res.raise_for_status()
        except:
            run=False
            
           
        # Creates a BeautifulSoup object for HTML parsing
        soup = BeautifulSoup(res.text, 'html.parser')
            
        num=soup.find_all('h3',{"class":'lvtitle'})
        
        if len(num)==0:
            run=False
            
        sites=[]
        for n in num:
            contents=n.contents
            for c in contents:
                href=c[u'href']
                sites.append(href)
                break
        
        for s in sites:
            resS = requests.get(s)
#            print(s)
            soupS = BeautifulSoup(resS.text, 'html.parser')
            priceI=soupS.find_all("span",{"itemprop":"price"})
            priceII=soupS.find_all("span",{'id':"mm-saleDscPrc"})
            #priceI=soupS.find_all("p",{"data-detail":"price"})
            descI=soupS.find_all("title")
            
            loc=soupS.find_all("span",{'itemprop':'availableAtOrFrom'})
            seller=soupS.find_all("span",{'class':'mbg-nw'})
            objImg=soupS.find_all("meta",{'name':'twitter:image'})
            
            descp=''
            prce=''
            location=''
            sellR=''
            obImg=''
            
            ccp=''
            for p in priceI:
                for cc in p.contents:
                    try:
                        ccpT=cc.split(" ")
                        if len(ccpT)>1:
                            ccp=ccpT[1]
                        else:
                            ccp=ccpT[0].strip()
                    except:
                        print('stop')
                        
                    price[s]=ccp
                    prce=str(ccp.encode('utf-8').strip())
                    break

            for d in descI:
                for cc in d.contents:
                    desc[s]=str(cc.encode('utf-8').strip())
                    descp=str(cc.encode('utf-8').strip())
            
                
            if prce=='':
                for pp in priceII:
                    for cc in pp.contents:
                        try:
                            ccpT=cc.split(" ")
                            if len(ccpT)>1:
                                ccp=ccpT[1]
                            else:
                                ccp=ccpT[0].strip()
                        except:
                            print('stop')
                        
                        price[s]=ccp
                        prce=str(ccp.encode('utf-8').strip())
                        break
                
            for l in loc:
                for cc in l.contents:
                    locs[s]=str(cc)
                    location=str(cc)
            
            for se in seller:
                for cc in se.contents:
                    ssT=str(cc)
                    sell[s]=ssT
                    sellR=ssT
            
            
            for img in objImg:
                content= img['content']
                obImg=str(content.encode('utf-8').strip())
            
            if run is True:
                prinItem(descp,prce,location,s,sellR,obImg)
                    
            
    return run


            
def prinItem(descP,priceP,locP,linkP,sellerP,image):

        d=descP.split("|")[0].strip()
        p=priceP
        l=locP.encode('utf-8').strip()
        o=linkP.encode('utf-8').strip()
        ss=sellerP.encode('utf-8').strip()
        img=image
            
                
        writer.writerow({'Object':str(d),'Price':str(p),'Location':str(l),'Seller':str(ss),'Image':str(img),
                         'Link':str(o).encode('utf-8').strip()})
            
'''
The file output path for printing results (to the src level of this project)
@return rn- the output file path to use to the src level
''' 
def filenameToOutput():
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        
        return pn
    
    
''''
The main to launch this module
'''
price={}
desc={}
locs={}
sell={}

if __name__ == '__main__':
    fieldnames = ['Object','Price','Location','Seller','Image','Link']
    
    
    filename=os.path.join(filenameToOutput(),'output','scrapedOutput.csv')
    
    #here we open the results which will the name of cultures scraped from eBay
    with open(filename, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()  
        make_urls()
    
        print('Finished')

