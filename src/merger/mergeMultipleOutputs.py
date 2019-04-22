'''
Module used to merge multiple outputs from the named entity recognition and dictionary search outputs (see nlp.nameEntityRecog.py).

Created on Feb 11, 2019

@author: 
'''

import csv
import os


#dates of outputs
dates=[]

#object descriptions from outputs
objects=[]

#prices of objects from outputs
prices=[]

#location information of where objects were sold
locations=[]

#cultural categories in which objects belong to
categories=[]

#types of objects in which objects can be affiliated to
objectTypes=[]

#the links to the objects from the outputs
links=[]

#the total input description data from objects used to track duplicates
totalThings=[]

#the material types associated with objects
matTypes=[]

#prices of duplicate objects are traced using what is stored here
priceExtra=[]

'''
Method to load input files from the totalData folder and combine into one output file
@return totals- the data merged and to be given in an output.
'''
def loadData():
    
    #This code changes the current directory so relative paths are used
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'totalData')
    
    totals=[]
   
    
  
    for fil in os.listdir(pathway):
        with open(os.path.join(pathway,fil),'rU') as csvfile:
            reader = csv.DictReader(csvfile)
            print(csvfile)
             
            for row in reader:
                date=row['Date']
                obj=row['Object']
                price=row['Price']
                location=row['Location']
                cat=row['Category']
                objT=row['Object Type']
                matType=row['Material']
                link=row['Link']
                
                totalThing=obj
                
                if totalThing in totalThings:
                    if price in priceExtra:
                        continue
                
                else:
                    priceExtra.append(price)
                    totalThings.append(totalThing)
                    dates.append(date)
                    objects.append(obj)
                    prices.append(price)
                    locations.append(location)
                    categories.append(cat)
                    objectTypes.append(objT)
                    links.append(link)
                    matTypes.append(matType)
                
                
    return totals            

'''
Method to print results of the merged files
'''                 
def printResults():
    
    fieldnames = ['Date','Object','Price','Location','Category','Object Type','Material','Link']

    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    fileOutput=os.path.join(pn,'output',"namedEntityMerged.csv")
    
    with open(fileOutput, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()      
    
        for i in range(0,len(objects)):
           
            writer.writerow({'Date': str(dates[i]),'Object':str(objects[i]),'Price':str(prices[i]),'Location':str(locations[i]),'Category':
                str(categories[i]),'Object Type':str(objectTypes[i]),'Material':str(matTypes[i]),'Link':str(links[i])})
   
#           writer.writerow({'Object':str(objects[i]),'Price':str(prices[i]),'Location':str(locations[i]),'Link':str(links[i])})

'''
Method to run the module
'''  
def run():
    results=loadData()
    printResults(results)
    print("Finished")
   
if __name__ == '__main__':
    run()