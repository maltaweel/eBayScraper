'''
Created on Jan 17, 2019

@author: mark
'''

import pysal
import os
import csv


oldNodes={}
nodes={}
links=[]
nodesS=[]
linkz={}

'''
Load the data and creating the links for the network from street segment file.
@param fileName the shapefile name to assess.
'''
def load(dbfName,csvName):
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
        
    #The data file path is now created where the data folder and dataFile.csv is referenced
    filename=os.path.join(pn,'data',dbfName)
        
    dbf = pysal.open(filename)
    
    countries = dbf.by_col('NAME')
    
    pathway=os.path.join(pn,'data',csvName)

    results={}
    
        
    with open(pathway) as csvfile:
            reader = csv.DictReader(csvfile)
            
            i=0
            for row in reader:
                    if i==0:
                        i+=1
                        
                    else:
                        print('')
                        


                        
def run():
    dbf='TM_WORLD_BORDERS-0.3.dbf'
    csvF='namedEntity.csv'
    
    load(dbf,csvF)
    
    print("Finished")
   
if __name__ == '__main__':
    run()

