import csv
import os
import pysal
import sys


def load(dbF,csvName): 
    
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
        
    #The data file path is now created where the data folder and dataFile.csv is referenced
    filename=os.path.join(pn,'data',dbF)
    
    shp = pysal.open(filename.replace('.csv','.shp'))
    
    
    pathway=os.path.join(pn,'data',csvName)

    results={}
    prices={}
    category={}
        
    with open(pathway) as csvfile:
            reader = csv.DictReader(csvfile)
            
            i=0
            for row in reader:
                    if i==0:
                        i+=1
                        
                    else:
                        date=row['Date']
                        obj=row['Object']
                        price=row['Price']
                        cat=row['Category']
                        link=row['Link']
                        loc=row['Location']
                        
                        ii=0
                        
                        with open(filename) as csvf:
                            readerr = csv.DictReader(csvf)
                             
                             
                            for r in readerr:
                            
                                rslt=[]
                                prc=[]
                                ctg=[]
                                c=r['NAME']
                                if c in results:
                                    rslt=results[c]
                                    prc=prices[c]
                                    rslt.append(loc)
                                    prc.append(price)
                                    ctg.append(cat)
                                
                                else:
                                    rslt.append(loc)
                                    prc.append(price)
                                    ctg.append(cat)
                            
                                results[c]=rslt
                                prices[c]=prc
                                category[c]=ctg
                            
                                s=shp[i]
                            
                            
                            ii+=1
                               
                                
                        
                        


                        
def run():
    dbf='TM_WORLD_BORDERS-0.3.dbf'
    csvF='namedEntity.csv'
    
    load(dbf,csvF)
    
    print("Finished")
   
if __name__ == '__main__':
    run()

