'''
Module used to merge multiple scraped  data from eBay.
Created on Feb 11, 2019
@author: 
'''

import csv
import os

#The object descriptions to incorporate
objects=[]

#The prices of objects to incorporate
prices=[]

#The location of objects to incorporate
locations=[]

#The links of objects to incorporate
links=[]

#Extra objects to track and remove
totalThings=[]

#List keeping track of extra prices for the same object descriptions used to remove data
priceExtra=[]

#data on sellers
sellers=[]

#image data
images=[]

news=[]
'''
Method to load data from input files in the totalData folder.
'''
def loadData():
    
    #This code changes the current directory so relative paths are used
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'totalData')
    
    totals=[]
   
    
  
    for fil in os.listdir(pathway):
        with open(os.path.join(pathway,fil),'rU') as csvfile:
            reader = csv.DictReader(x.replace('\0', '') for x in csvfile)
            print(csvfile)
            new=0
            for row in reader:   
                obj=row['Object']
                price=row['Price']
                location=row['Location']
                seller=row['Seller']
#                image=row['Image']
                link=row['Link']
                
                
#                seller=row['Seller']
                
                totalThing=obj.strip()
                
                if totalThing in totalThings:
                    if price in priceExtra:
                        continue
                
                else:
                    totalThings.append(totalThing)
                    priceExtra.append(price)
                    objects.append(obj)
                    prices.append(price)
                    locations.append(location)
#                    sellers.append(seller)
                    sellers.append(seller)
#                    images.append(image)
                    links.append(link)
                    if 'namedEntityToal.csv' in fil:
                        new=1
                    news.append(new)
                        
          
                
                
    return totals            
     
'''
Method to print the results of the output
'''                   
def printResults():

    fieldnames = ['Object','Price','News','Seller','Location','Link']
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    fileOutput=os.path.join(pn,'output',"namedEntityTotal.csv")
    
    with open(fileOutput, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)
        
        writer.writeheader()      
    
        for i in range(0,len(objects)):
            
            writer.writerow({'Object':str(objects[i]),'Price':str(prices[i]),'News':str(news[i]),
                             'Seller':str(sellers[i]),'Location':str(locations[i]),'Link':str(links[i])})
'''
Method to run the module
'''           
def run():
#    train_model()
    loadData()
    printResults()
    print("Finished")
   
if __name__ == '__main__':
    run()