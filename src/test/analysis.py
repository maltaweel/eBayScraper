'''
Created on May 9, 2019

@author: mark
'''
import os
import csv
import numpy

returns={}
objects={}
materials={}
totals=0

rs=[]
ob=[]
mts=[]
seller={}

def loadFile():
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'output','namedEntityMerged.csv')

    
    with open(os.path.join(pathway),'rU') as csvfile:
      
        reader = csv.DictReader(csvfile)
        
        for r in reader:
            
            c=r['Category']
            o=r['Object Type']
            m=r['Material']
            sell=r['Seller']
            p=float(r['Price'])
            
            sc=c.split("|")
            so=o.split("|")
            sm=m.split("|")
            
            if sell !='':
                
                total=0
                if sell in seller:
                    total=seller[sell]
                    
                seller[sell]=total+p
            
            
def printResults():
    
   # fieldnames = ['Culture','Object','Material','Number1',"Number2","Number3"]
    fieldnames = ['Type',"Indicator","Total",'Mean','Median','SD','Min',"Max", "Seller"]
   #fieldnames = ['Egyptian',"Unknown",'Roman','Near East','Vessels']
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    fileOutput=os.path.join(pn,'output',"analysisOutput.csv")
    
    #write output file including data from results of the NER/dictionary analysis
    with open(fileOutput, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()  
        
        for i in range(0,len(ob)):
             
            if i < len(rs):
                ott=rs[i]
                ost=returns[ott]
                
                total=numpy.sum(ost)
                mean=numpy.log(numpy.mean(ost))
                median=numpy.log(numpy.median(ost))
                sd=numpy.log(numpy.std(ost))
                mn=numpy.log(numpy.min(ost))
                mx=numpy.log(numpy.max(ost))
                
                writer.writerow({'Type': ott,'Indicator':str('a'),'Total':total,'Mean':mean,'Median':median,'SD':sd,'Min':mn,'Max':mx, "Seller":''})
            
               
            if i < len(ob):
                ot=ob[i]
                oss=objects[ot]
                
                
                mean=numpy.mean(oss)
                median=numpy.log(numpy.median(oss))
                sd=numpy.log(numpy.std(oss))
                mn=numpy.log(numpy.min(oss))
                mx=numpy.log(numpy.max(oss))
                total=numpy.sum(oss)
                
                writer.writerow({'Type': ot,'Indicator':str('b'),'Total':total,'Mean':mean,'Median':median,'SD':sd,'Min':mn,'Max':mx,"Seller":''})
                    
            if i < len(mts):
                mt=mts[i]
                mat=materials[mt]
                total=numpy.sum(mat)
                mean=numpy.log(numpy.mean(mat))
                median=numpy.log(numpy.median(mat))
                sd=numpy.log(numpy.std(mat))
                mn=numpy.log(numpy.min(mat))
                mx=numpy.log(numpy.max(mat))
                
                
                writer.writerow({'Type': mt,'Indicator':str('c'),'Total':total,'Mean':mean,'Median':median,'SD':sd,'Min':mn,'Max':mx,"Seller":''})  
                    
   
loadFile() 
printResults()
print("Finished")
           
            
            
            
        

