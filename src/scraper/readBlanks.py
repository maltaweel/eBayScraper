'''
Created on Mar 4, 2019

@author: mark
'''

import csv
import os

def readFile():
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'output','canFindEntity.csv')

    
   
    with open(os.path.join(pathway),'rU') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                obj=row['Object']
                
