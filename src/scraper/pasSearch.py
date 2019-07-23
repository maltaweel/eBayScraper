'''
Created on Jun 28, 2019

@author: mark
'''

import os
import csv
from bs4 import BeautifulSoup
import requests

site='https://finds.org.uk/database/search/results/q/'

database='https://finds.org.uk/'


#partTwo='Spindle+Whorl+Early+Medieval+950+-1050'

def loadSearchText():
    fInput=filenamePath()+'/output/'
    
    with open(os.path.join(fInput,'namedEntityUK.csv'),'rU',buffering=0) as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    description=row['Object Type']
                    
                    description=description.strip()
                    search=site+description.replace("|","+")
                    results=runSearch(search)
                    
                    if results =='':
                        continue
                    else:
                        print(results)
                
                    data=runResults(results)
                    
                    printResults(data)

def printResults(data):
    
    
    link=data['link']
    content=data['content']
    image=data['image']
    
                   
    writer.writerow({'Object':str(content),'Image':str(image),'Link':str(link)})
        
def runSearch(search):
    links=[]
    
    run=True
    res = requests.get(search)
    try:
        res.raise_for_status()
    except:
        run=False
    
    if run==False:
        return ''
         
    soup = BeautifulSoup(res.text, 'html.parser')
    entry=soup.find_all('div',{"id":'preview'})
    
    for t in entry:
        for i in t.find_all('p'):
            
            
            for t in i.find_all('a'):
                links.append(t)
            
             
    return links
    
def runResults(results):
    data={}
    for l in results:
        link=database + l['href']
        data['link']=link
        res = requests.get(link)
        try:
            res.raise_for_status()
        except:
            continue
        
        soup = BeautifulSoup(res.text, 'html.parser')
        entry=soup.find_all('head')
        
        for e in entry:
            desc=e.find_all('meta',{'name':'description'})
            
            for c in desc:
                data['content']=c['content']
            
    
        images=soup.find_all('div',{'id':'imagepane'})
        
        
        for i in images:
            imgs=i.find_all('img')
            for x in imgs:
                ll=x['src']
                if 'https' in ll:
                    data['image']=ll
                
            
    return data
    
'''
The file output path for printing results (to the src level of this project)
@return rn- the output file path to use to the src level
''' 
def filenamePath():
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        
        return pn

''''
The main to launch this module
'''
if __name__ == '__main__':
    
    fieldnames = ['Object','Image','Link']
    
    
    filename=os.path.join(filenamePath(),'output','pasSiteOutput.csv')
    
    #here we open the results which will the name of cultures scraped from eBay
    with open(filename, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()  
        loadSearchText()
    
        print('Finished')