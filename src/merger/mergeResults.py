import csv
import os
import pysal


def load(dbF,csvName): 
    
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
        
    #The data file path is now created where the data folder and dataFile.csv is referenced
    filename=os.path.join(pn,'data',dbF)
    
    dbf = pysal.open(filename)
    
    countries = dbf.by_col('NAME')
    
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
                        
                        for c in countries:
                            
                            rslt=[]
                            prc=[]
                            ctg=[]
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
                               
                                
                        
                        


                        
def run():
    dbf='TM_WORLD_BORDERS-0.3.dbf'
    csvF='namedEntity.csv'
    
    load(dbf,csvF)
    
    print("Finished")
   
if __name__ == '__main__':
    run()

