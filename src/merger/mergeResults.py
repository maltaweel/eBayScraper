import csv
import os
import pysal
from dbfpy import dbf


def load(dbF,csvName): 
    
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
        
    #The data file path is now created where the data folder and dataFile.csv is referenced
    filename=os.path.join(pn,'shp',dbF)
    
    db = pysal.open(filename)
    shp = pysal.open(filename.replace('.dbf','.shp'))
    
    
    pathway=os.path.join(pn,'data',csvName)

    results={}
    prices={}
    category={}
    place={}
        
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
                        
#                        with open(filename) as csvf:
#                            readerr = csv.DictReader(csvf)
                             
                        
                        for r in db.by_col['NAME']:
                            
                            if r.lower() in loc.lower():
                                rslt=[]
                                prc=[]
                                ctg=[]
                                if r in results:
                                    rslt=results[r]
                                    prc=prices[r]
                                    ctg=category[r]
                                    
                                rslt.append(loc)
                                prc.append(float(price))
                                ctg.append(cat)
                            
                                results[r]=rslt
                                prices[r]=prc
                                category[r]=ctg
                            
                                s=shp[ii]
                                try:
                                    place[r]=s[0][3]
                                except:
                                    print("stop")
                            
                            
                        ii+=1
                               
                                
            return results, prices, category, place           
                        

def finalizeResults(results,prices,category,place):
    
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    filename=os.path.join(pn,'shp','output.dbf')
    
    totalCats={}
    names={}
    lcs={}
    
    totals={}
    location=[]
    
    i=0
    for r in results:
        price=prices[r]
        cat=category[r]
        
        listCats={}
        for c in cat:
            if c in listCats:
                listCats[c]=listCats[c]+1
            else:
                listCats[c]=1
            names[c]=c
            
        totalCats[r]=listCats
               
        total=sum(price)
        totals[r]=total
        
        shp=place[r]
        lcs[shp]=r   
        location.append(shp)
         
        i+=1
        
    db = dbf.Dbf(filename, new=True)
    db.addField( ("NAME", "C", 15),("TOTAL","F",10,10),("TOP","C",15))

    for shp in location:
        
        r=lcs[shp]
        listCats=totalCats[r]
        t=totals[r]
    
        top=''
        ss=0
        
        for n in listCats:
            lst=listCats[n]
            
            if lst>ss:
                ss=lst
                top=n
        
        rec = db.newRecord()
        rec["NAME"] = r
        rec["TOTAL"] = t
        rec["TOP"] = top
        rec.store()

    db.close()
    
                        
def run():
    dbf='TM_WORLD_BORDERS-0.3.csv'
    csvF='namedEntity.csv'
    
    results, prices, category, place=load(dbf,csvF)
    
    finalizeResults(results,prices,category,place)
    
    print("Finished")
   
if __name__ == '__main__':
    run()

