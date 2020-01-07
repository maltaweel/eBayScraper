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

#seller data
sellers=[]

'''
Method to load input files from the totalData folder and combine into one output file
'''
def loadData():
    
    #This code changes the current directory so relative paths are used
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'totalData')
    
    #loop through the directory of files
    for fil in os.listdir(pathway):
        with open(os.path.join(pathway,fil),'rU') as csvfile:
            reader = csv.DictReader(x.replace('\0', '') for x in csvfile)
            print(csvfile)
             
            #get data from rows
            for row in reader:
                
                date=row['Date']
                obj=row['Object']
                price=row['Price']
                location=row['Location']
                cat=row['Category']
                objT=row['Object Type']
                matType=row['Material']
                link=row['Link']
                seller=row['Seller']
                
                totalThing=obj
                
                #this will determine what a duplicate is and remove
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
                    sellers.append(seller)
                
'''
Method to print results of the merged files
'''                 
def printResults():
    
    fieldnames = ['Date','Object','Price','Location','Category','Object Type','Material','Seller','Link']

    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    
    #output is namedEntityMerged.csv
    fileOutput=os.path.join(pn,'output',"namedEntityMerged.csv")
    
    #opens the output file and then puts the output in
    with open(fileOutput, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()      
    
        for i in range(0,len(objects)):
           
            writer.writerow({'Date': str(dates[i]),'Object':str(objects[i]),'Price':str(prices[i]),'Location':str(locations[i]),'Category':
                str(categories[i]),'Object Type':str(objectTypes[i]),'Material':str(matTypes[i]),'Seller':str(sellers[i]),'Link':str(links[i])})
   
#           writer.writerow({'Object':str(objects[i]),'Price':str(prices[i]),'Location':str(locations[i]),'Link':str(links[i])})

'''
Method to run the module
'''  
def run():
    #first load the data
    loadData()
    
    #then print the results
    printResults()
    
    print("Finished")
   
if __name__ == '__main__':
    run()