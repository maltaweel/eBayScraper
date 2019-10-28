'''
Module used to analyse outputs from eBay NER methodology and visualize spatially those outputs.

Created on Feb 11, 2019

@author: 
'''

import csv
import os
import pysal
import operator
from dbfpy import dbf

sellerT={}

#cultrual terms to be assessed as categorisation
words={'roman':'ROMAN','byzantine':'BYZANTINE','islamic':'ISLAMIC',  'egyptian':'EGYPTIAN',
       'greek':'GREEK','viking':'VIKING','revolutionary':"REVOLUTION", 'renaissance':'RENAISSANC',
       'khazar':'KHAZAR','mogul':'MOGUL','bronze age':'BRONZE_AGE','scythian':'SCYTHIAN',
       'iron age':'IRON_AGE','russian':'RUSSIA','medieval':'MEDIEVAL','celtic':'CELT', 'central asia': 'CENT_ASIA',
       'america':'AMERICA','pre-historic':'PRE_HISTOR','china':'CHINA','japan':'JAPAN','buddhist':'BUDDHIST','near east':'NEAR_EAST',
       'mongol':'MONGOL','africa':'AFRICA','medieval':'MEDIEVAL','european':'EUROPEAN','cambodian':'CAMBODIAN',
       'other':'OTHER','india':'INDIA'}

#types of objects categorised in the outputs
objTL={'jewellery':'JEWELLERY','vessel':'VESSEL','statue':'STAT_FIG','weapon':'WEAPON','text':'TEXT',
      'clothing':'CLOTHING','household':'HOUSEHOLD','coin':'COIN','mask':'MASK','religious':'RELIGIOUS','tool':'TOOL','painting':'PAINTIN',
      'portrait':"PORTRAIT",'feature':'FEATURE','decoration':'DECORATION','OTHER':'OTHER_O'}

#material types categorised in the outputs
mat={'terracotta':"TERRACOTTA",'metal':"METAL",'glass':"GLASS",'stone':"STONE",'wood':'WOOD','bone':'BONE','ivory':'IVORY','leather':'LEATHER',
     'other':'OTHER','papyrus':'PAPYRUS'}

'''
Method that loads a dbf file from a .shp file and finds the correct categories to assess and country-level data from the NER output file. 
The end results is a dictionary that organizes the data according to the country in which it relates to.

@param dbF- the .dbf file used from the shapefile to get categories and countries to affiliate the output data.
@param csvName- the csv output file from the NER-based methodology and associated with given countries.
@return results- the location results from the output file
@return prices-  the price results from the output .csv file
@return category- the cultural category results from the output .csv file
@return place- the places from the shape file
@return objTs- the object types from the output .csv file
@return matT-  the material types from the output .csv file
'''
def load(dbF,csvName): 
    
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
        
    #The data file path is now created where the data folder and dataFile.csv is referenced
    filename=os.path.join(pn,'shp',dbF)
    
    db = pysal.open(filename)
    shp = pysal.open(filename.replace('.csv','.dbf'))
    
    
    pathway=os.path.join(pn,'output',csvName)

    results={}
    prices={}
    category={}
    place={}
    objTs={}
    matT={}
   
    
    #open the csv and go through the results
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
                        sel=row['Seller']
                        
                        if loc=='':
                            continue
                        ii=0
                        l=loc.split(",")
                        ll=l[len(l)-1].strip().lower()
                        
                        #results will be matched to the country in the dbf
                        #this is done by looping through the dbf
                        for r in db.by_col['NAME']:
                            
                            if ll in r.lower():
                                if r == 'United States Virgin Islands' or r=='United States Minor Outlying Islands':
                                    continue
                                
      #                          print(loc+" : "+r)
                                
                                rslt=[]
                                prc=[]
                                ctg=[]
                                objT=[]
                                mtT=[]
                                sell=[]
                                sellT={}
                                if r in results:
                                    rslt=results[r]
                                    prc=prices[r]
                                    ctg=category[r]
                                    objT=objTs[r]
                                    mtT=matT[r]
                                    sellT=sellerT[r]
                                    
                                    
                                rslt.append(loc)
                                prc.append(price)
                                ctg.append(cat)
                                    
                                objT.append(objectT)
                                
                                sell.append(sel)
                                mtT.append(mat)
                                
                            
                                results[r]=rslt
                                prices[r]=prc
                                category[r]=ctg
                                objTs[r]=objT
                                matT[r]=mtT
                               
                                s=shp[ii]
                                
                                place[r]=s
                                
                                selT=price
                                if sel in sellT:
                                    selT+=sellT[sel]
                                    
                
                                
                                sellT[sel]=selT
                                
                                sellerT[r]=sellT
                            
                            ii+=1
                               
                            
    return results, prices, category, place, objTs, matT           
                        
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
        
        sell=sellerT[r]
        
        
        a=max(sell.iteritems(), key=operator.itemgetter(1))[0]
        vp=sell[a]
        
            
        rec['TopSeller']=a
        rec['TopSellerT']=vp
        
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
    dbf='TM_WORLD_BORDERS-0.3.csv'
    csvF='namedEntityMerged.csv'
    
    #first load the data from namedEntityTotal.csv
    results, prices, category, place, objTs, matT=load(dbf,csvF)
    
    #then output results to the .shp file, which is the same as the .csv file TM_WORLD
    finalizeResults(results,prices,category,place,dbf,objTs, matT)
    
    print("Finished")
   
if __name__ == '__main__':
    run()

