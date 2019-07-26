'''
Module used to analyse outputs from eBay NER methodology and visualize spatially those outputs.

Created on Feb 11, 2019

@author: 
'''

import csv
import os
import pysal
from dbfpy import dbf
from fiona.fio.cat import cat
from Lib.types import ObjectType

#types of objects categorised in the outputs
objTL={'jewellery':'JEWELLERY','coin':"COIN",'brooch':"BROOCH",'silver':'SILVER','gold':'GOLD'}

names={}
counties={}

namesUK={}
countiesUK={}

def loadShape(data):
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
        
    #The data file path is now created where the data folder and dataFile.csv is referenced
    filename=os.path.join(pn,'towns',data)
    
    with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
    
            for r in reader:
                name=r['name']
                county=r['countyname']
                
                c={}
                if county in counties:
                    c=counties[county]
                
                c[name]=0.0
                counties[county]=c
                
                names[name]=0.0
                
                
                    
               
     
'''
Method that loads data output and matches to the town and county level data in the UK.

@param csvName- the csv output file from the NER-based methodology and associated with given countries.

'''
def load(csvName): 
    
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
        
   
    pathway=os.path.join(pn,'output',csvName)

    results={}
    prices={}
    category={}
    place={}
    objTs={}
    matT={}
    
    #open the file and go through the results
    with open(pathway) as csvfile:
            reader = csv.DictReader(csvfile)
            
            i=0
            for row in reader:
                    if i==0:
                        i+=1
                        
                    else:
                        date=row['Date']
                        obj=row['Object']
                        price=float(row['Price'])
                        cat=row['Category']
                        link=row['Link']
                        loc=row['Location']
                        objectT=row['Object Type']
                        mat=row['Material']
                        
                        if loc=='':
                            continue
                        ii=0
                        l=loc.split(",")
                        
                        town=l[0]
                        
                        county=''
                        if len(l)>2:
                            county=l[1]
                        
                        countT=False  
                        if county in counties:
                            c=counties[county]
                            
                            if county in countiesUK:
                                cUK=countiesUK[county]
                                
                            else:
                                cUK={}
                                countiesUK[county]=cUK
                            
                                
                            if town in c:
                                objTypeUK=[]
                                priceUK=[]
                                
                                if town in cUK:
                                    tUK=cUK[town]
                                    objTypeUK=tUK['objectType']
                                    priceUK=tUK['price']
                                else:
                                    tUK={}
                                    
                                objTypeUK.append(objectT)
                                priceUK.append(price)
                                tUK['objectType']=objTypeUK
                                tUK['price']=priceUK
                                cUK[town]=tUK
                                countiesUK[county]=cUK
                                countF=True
                           
                        if countF is False:
                            if town in names:
                                if town in namesUK:
                                    t=namesUK[town]
                                    objTypeUK=[]
                                    priceUK=[]
                                else:
                                    t={}
                                    objTypeUK=t['objectType']
                                    priceUK=t['price']
                                
                                objTypeUK.append(objectT)
                                priceUK.append(price)
                                t['objectType']=objTypeUK
                                t['price']=priceUK
                                namesUK[town]=t   
                            
                            
'''
Method to associate data with appropriate dictionaries and merge results for assessment on price.
@param objT- categories retrieved from output data
@param objTT- category types assessed
@param price- the price dictionary for objects

@return lisN a dictionary of objects and types with relevant prices 
'''
def locationsO(objT,objTT,price):
    
    lisN={}
    ii=0
    for n in objT:
        nns=n.split("| ")
        
        for nn in nns:
            nn=nn.lower()
            if nn is '':
                continue
            elif nn.strip() == '?':
                nn='OTHER'
                if 'OTHER' in lisN:
                    lisN[nn]=lisN[nn]+price[ii]
                else:
                    lisN[nn]=price[ii]
                
                continue
            
            try:
                nSn=objTT[nn.strip()]
            except Exception, e:
                print('error: ')
                print( e)
                continue
                
            if nSn in lisN:
                v=lisN[nSn]+price[ii]
                lisN[nSn]=v
            else:
                try:
                    lisN[nSn]=price[ii]
                except Exception, e:
                    print('error: ')
                    print(e)
        
        ii+=1
            
    return lisN  

'''
Method takes .csv and .dbf outputs and integrates the results to the appropriate country-level output based on aggregating the 
results from the NER output. The outputs include material type, culture type, and type of objects that are found in a 
given country selling the objects. The total dollar value is then determined for those categories in a given country.

@param results- the location results to assess from the output file
@param prices- the price results to assess
@param category- the cultural category  results to assess
@param place- the country to associate data with
@param dbF- the dbF file used for the shapefile
@param objTs- the object types (i.e., object categories) from results on cultural objects
@param matT- the material types from results
'''      
def finalizeResults(results,prices,category,place,dbF,objTs, matT):
    
    #this will output back to the shapefile of the world
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    filename=os.path.join(pn,'shp',dbF.replace('.csv','.shp'))
         
    db = dbf.Dbf(filename.replace('.shp','.dbf'),ignoreErrors=True)
    shp = pysal.open(filename,'w')
    
   
    totalCats={}
   
    
    totals={}
    location=[]
    
    i=0
    recs=[]
    
    #loop through the results from the csv
    for r in results:
        rec=''
        for re in db:
            nm=re['NAME']
            if nm in r:
                rec=re
                break
            else:
                recs.append(re)
                continue    
              
        price=prices[r]
        cat=category[r]
        objT=objTs[r]
        mtT=matT[r]
        
        objsN=locationsO(objT,objTL,price)
        matsN=locationsO(mtT,mat,price)
        
        listCats={}
        
        #below code goes through the material, cultural, and type of object data
        ii=0
        for c in cat:
            ccs=c.split(" | ")
            
            for cc in ccs:
                cc=cc.replace("|","")
                cc=cc.lower().strip()
                if cc =='':
                    continue
                if cc in listCats:
                    listCats[cc]=listCats[cc]+price[ii]
                else:
                    listCats[cc]=price[ii]
            
            ii+=1
        
        for c in listCats: 
            try:
                if c =='':
                    continue
                sCats=listCats[c]
                if  c=='?':
                    c='OTHER'
                    rec[c]=sCats
                    continue
                
                w=words[c]
                rec[w]=sCats
            except Exception, e:
                print('error: ')
                print(e) 
                    
        
        top=''
        ss=0
        
        for n in listCats:
            lst=listCats[n]
            
            if lst>ss:
                ss=lst
                top=n
            
        totalCats[r]=listCats
               
        total=sum(price)
        totals[r]=total
        s=place[r]
        
        for t in objsN:
            if t=='?':
                t='OTHER'
                
            rec[t]=objsN[t]
        
        for m in matsN:
            mm=mat[m.lower()]
            rec[mm]=matsN[m]
       
        #the total sales data is kep here for each country
        rec["TOTAL"] = total
        
        #the top selling culture is stored
        rec["TOP"] = top.capitalize()
        rec.store()
        
    #    print(s)
        location.append(s)
         
        i+=1

           
    db.close()
    
'''
Method to run the module
'''                
def run():
    dbf='placesUK.csv'
    csvF='namedEntityMergedUK.csv'
    loadShape(dbf)
    
    #first load the data from namedEntityTotal.csv
    load(csvF)
    
    '''
    #then output results to the .shp file, which is the same as the .csv file TM_WORLD
    finalizeResults(results,prices,category,place,dbf,objTs, matT)
    '''
    print("Finished")
   
if __name__ == '__main__':
    run()

