'''
Created on Mar 25, 2019

@author: mark
'''
import os
import random
import csv

def selectRandom():
    
    print "run random"
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'output','namedEntity.csv')

    returns=[]
    
    row_count=0
    with open(os.path.join(pathway),'rU') as csvfile:
        row_count = sum(1 for row in csvfile)
    
    with open(os.path.join(pathway),'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        rows=[r for r in reader]
    
        numbers=[]
        for i in range(1,400):
            numbers.append(random.randint(1,row_count))
    
        

           
        for x in numbers:
            returns.append(rows[x])
                
        
    return returns

def printResults(results):
    
    fieldnames = ['Date','Object','Price','Location','Category','Object Type','Material','Link']
     
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    fileOutput=os.path.join(pn,'output',"randomSelectionTest.csv")
    
    with open(fileOutput, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()    
        for d in results:
           
            
            res0=d['Date']
            
            res1=d['Object']
            res2=d['Price']
            res3=d['Location']
            res4=d['Category']
            res5=d['Object Type']
            res6=d['Material']
            res7=d['Link']
            
            writer.writerow({'Date': str(res0),'Object':str(res1),'Price':str(res2),'Location':str(res3),
                             "Category":str(res4),'Object Type':str(res5),'Material':
                             str(res6),'Link':str(res7)})  
    
    
def run():
    results=selectRandom()
    printResults(results)
   
if __name__ == '__main__':
    run()

