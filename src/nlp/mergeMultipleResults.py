'''
Created on Feb 11, 2019

@author: mark
'''

import csv
import os
from docutils.nodes import row

title=''


def loadData():
    
    #This code changes the current directory so relative paths are used
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'totalData')
    
    totals=[]
   
    
  
    for fil in os.listdir(pathway):
        with open(os.path.join(pathway,fil),'rU') as csvfile:
            reader = csv.DictReader(csvfile)
                
                
            i=0
            for row in reader:
                if i==0:
                    title=row
                    i+=1
                    
                else:
                    if row in totals:
                        continue
                    else:
                        
                        totals.append(row)
    
    return totals            
                        
def printResults(results):
    
    fieldnames = title
     
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    fileOutput=os.path.join(pn,'output',"namedEntityMerged.csv")
    
    with open(fileOutput, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()      
    
        for d in results:
            writer.writerow({fieldnames: str(d)})
            
def run():
#    train_model()
    results=loadData()
    printResults(results)
    print("Finished")
   
if __name__ == '__main__':
    run()