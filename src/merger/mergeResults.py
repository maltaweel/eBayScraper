import csv
import os
import pysal
from dbfpy import dbf

words={'roman':'ROMAN','byzantine':'BYZANTINE','islamic':'ISLAMIC',  'egyptian':'EGYPTIAN',
       'greek':'GREEK','viking':'VIKING','revolutionary':"REVOLUTION", 'renaissance':'RENAISSANC',
       'khazar':'KHAZAR','mogul':'MOGUL','bronze age':'BRONZE_AGE',
       'iron age':'IRON_AGE','russian':'RUSSIAN','celt':'CELT',
       'america':'AMERICA','pre-historic':'PRE_HISTOR','china':'CHINA','japan':'JAPAN','buddhist':'BUDDHIST','near east':'NEAR_EAST',
       'mongul':'MONGUL','indus':'INDUS'}


objTL={'jewellery':'JEWELLERY','vessel':'VESSEL','statue':'STATUE','weapon':'WEAPON','text':'TEXT',
      'clothing':'CLOTHING','household':'HOUSEHOLD','coin':'COIN','mask':'MASK','religious':'RELIGIOUS','tool':'TOOL'}

def load(dbF,csvName): 
    
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
        
    #The data file path is now created where the data folder and dataFile.csv is referenced
    filename=os.path.join(pn,'shp',dbF)
    
    db = pysal.open(filename)
    shp = pysal.open(filename.replace('.csv','.dbf'))
    
    
    pathway=os.path.join(pn,'data',csvName)

    results={}
    prices={}
    category={}
    place={}
    objTs={}
        
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
                        objectT=row['Object Type']
                        
                        if loc.strip() =='':
                                continue
                        ii=0

                        for r in db.by_col['NAME']:
                                
                            if loc.lower().strip() in r.lower():
                                if r == 'United States Virgin Islands' or r=='United States Minor Outlying Islands':
                                    continue
                                rslt=[]
                                prc=[]
                                ctg=[]
                                objT=[]
                                if r in results:
                                    rslt=results[r]
                                    prc=prices[r]
                                    ctg=category[r]
                                    objT=objTs[r]
                                    
                                rslt.append(loc)
                                prc.append(float(price))
                                ctg.append(cat)
                                objT.append(objectT)
                            
                                results[r]=rslt
                                prices[r]=prc
                                category[r]=ctg
                                objTs[r]=objT
                               
                                s=shp[ii]
                                
                                place[r]=s
                                
                            
                            ii+=1
                               
                                
            return results, prices, category, place, objTs           
                        

def locationsO(objT,price):
    
    lisN={}
    ii=0
    for n in objT:
        if n is '':
            continue
        nn=objTL[n]
        if nn in lisN:
            v=lisN[nn]+price[ii]
            lisN[nn]=v
        else:
            lisN[nn]=price[ii]
        
        ii+=1
            
    return lisN  
        
def finalizeResults(results,prices,category,place,dbF,objTs):
    
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
        
        objsN=locationsO(objT,price)
        listCats={}
        
        ii=0
        for c in cat:
            if c in listCats:
                listCats[c]=listCats[c]+price[ii]
            else:
                listCats[c]=price[ii]
            
            ii+=1
        
        for c in listCats:   
            sCats=listCats[c]
            w=words[c]
            
            try:
                rec[w]=sCats
            except:
                print('case')
        
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
            rec[t]=objsN[t]
       
        rec["TOTAL"] = total
        rec["TOP"] = top.capitalize()
        rec.store()
        
        location.append(s)
         
        i+=1
    
   
        
           
    db.close()
    
    
    
                        
def run():
    dbf='TM_WORLD_BORDERS-0.3.csv'
    csvF='namedEntity.csv'
    
    results, prices, category, place, objTs=load(dbf,csvF)
    
    finalizeResults(results,prices,category,place,dbf,objTs)
    
    print("Finished")
   
if __name__ == '__main__':
    run()

