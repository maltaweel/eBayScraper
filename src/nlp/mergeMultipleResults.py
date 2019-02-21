'''
Created on Feb 11, 2019

@author: mark
'''

import csv
import os
from docutils.nodes import row

dates=[]
objects=[]
prices=[]
locations=[]
categories=[]
objectTypes=[]
links=[]
totalThings=[]


def loadData():
    
    #This code changes the current directory so relative paths are used
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'totalData')
    
    totals=[]
   
    
  
    for fil in os.listdir(pathway):
        with open(os.path.join(pathway,fil),'rU') as csvfile:
            reader = csv.DictReader(csvfile)
                
            for row in reader:
                date=row['Date']
                object=row['Object']
                price=row['Price']
                location=row['Location']
                cat=row['Category']
                objT=row['Object Type']
                link=row['Link']
                
                totalThing=object+" : "+price
                
                if totalThing in totalThings:
                    continue
                
                else:
                    totalThings.append(totalThing)
                    dates.append(date)
                    objects.append(object)
                    prices.append(price)
                    locations.append(location)
                    categories.append(cat)
                    objectTypes.append(objT)
                    links.append(link)
                
                
    return totals            
                        
def printResults(results):
    
    fieldnames = ['Date','Object','Price','Location','Category','Object Type','Link']
     
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    fileOutput=os.path.join(pn,'output',"namedEntityMerged.csv")
    
    with open(fileOutput, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()      
    
        for i in range(0,len(objects)):
           
            writer.writerow({'Date': str(dates[i]),'Object':str(objects[i]),'Price':str(prices[i]),'Location':str(locations[i]),'Category':
                str(categories[i]),'Object Type':str(objectTypes[i]),'Link':str(links[i])})
            
def run():
#    train_model()
    results=loadData()
    printResults(results)
    print("Finished")
   
if __name__ == '__main__':
    run()