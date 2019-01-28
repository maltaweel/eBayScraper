'''
Created on Jan 16, 2019

@author: mark
'''

import spacy
import csv
import nltk
import os
import random
import re
from datetime import datetime
from boto.mturk import price

spacy.prefer_gpu()
nlp = spacy.load('en')


objectTypes={'jewellery','vessel','statue','weapon','text','clothing','household','coin','mask'}

objectExtra={'weapon':'axe,sword,shield,sabre,helmet','vessel':'pottery,vessel,vase','statue':'statue,bust,idol,statuette,statuete,figurine,plaque',
             'jewellery':'necklace,bead,earing,amulet,seal,signet,bracelet','text':'tablet,inscription,writing',
             'clothing':'brooch,pin,sock,shoe,buckle','household':'altar,nail,hammer,glass,mirror','coin':'money'}

words={'roman','byzantine','islamic',  'egyptian','greek','viking','revolutionary', 'renaissance',
       'khazar','mogul','bronze age','iron age','russian','celt',
       'america','pre-historic','china','japan','buddhist','near east','mongul','indus'}

done=[]

equals={'celt':'seltic,scythian','egytpian':'egypt', 
        'america':'columbian,maya,aztec,native american,pre columbian,mexico,pre-columbian,indian',
        'islamic':'yemen,ottoman,afghan,khanate,arabic,koran,andalus,yamani,yemani,qajar,quran,persia,khazar,sulimani','buddhist':'bamiyan',
        'roman':'rome,romano', 'greek':'cypriot,athena,greco,mycenaean,macedonia',
         'russian':'russiam','indus':'indo,gandhara','pre-historic':'neolithic,pre historic,stone age,mesolithic,chalcolithic,paleolithic,palaeolithic',
         'near east':'near east,persian,bactrian,judaea,holy land,phoenician,mesopotamia,middle east,israel,canaanite,crusader',
         'egyptian':'pharao,ptolemaic','viking':'saxon,nordic',
         'china':'chinese','renaissance':'baroque,italian',
         'japan':'japanese','khazar':'kazar'}

entities={}

def findWholeWord(w,doc):

    if w.lower() in equals:
        d=equals[w]      
        wrds=d.split(",")
        
        for wo in wrds:
            t=re.findall(wo, doc.lower())
            if len(t)>0:
                return t
        
    
   
    t=re.findall(w, doc.lower())
    
   
    return t
    

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    newSent = nltk.pos_tag(sent)
    
    return newSent


def loadData():
    #This code changes the current directory so relative paths are used
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'data')

    results={}
    
    for word in words:
        
        for fil in os.listdir(pathway):
            with open(os.path.join(pathway,fil),'rU') as csvfile:
                reader = csv.DictReader(csvfile)
                
                
                i=0
                for row in reader:
                    if i==0:
                        i+=1
                    else:
                        obj={}
                        
                        objct=row['Object']
                        price=row['Price']
                        
                        totalP=objct+' '+price
                    
                            
                        df=findWholeWord(word,objct.lower())
                        
                        
                        if len(df)==0:
                            continue
                        
                        else:
                            if totalP in done:
                                continue
                            else:
                                done.append(totalP)
                                
                            if word in entities:
                                lst=entities[word]
                                lst.append(objct)
                                entities[word]=lst
                            
                            else:
                                lst=[]
                                lst.append(objct)
                                entities[word]=lst
                        
                        date1=objct.split("2019")
                        date2=objct.split("2018")
                        
                        dateKeep=''
                            
                        if len(date1)>1:
                            s1=date1[0].replace("Sold","").strip()
                            dateKeep=s1+" 2019"
                            
                        else:
                            s2=date2[0].replace("Sold","").strip()
                            dateKeep=s2+" 2018"
                        
                        
                        
                        location=row['Location']
                        link=row['Link']
                        
                        obj['date']=dateKeep
                        obj["object"]=objct
                        obj["price"]=price
                        obj['links']=link
                        obj['location']=location
                        obj['category']=word
                        
                        results[objct]=obj
                        
    return results

def lookAtText(results):
    
    for d in results:
        obj=results[d]
        
        objc=obj['object']
       
        resultType=''
        for x in objectTypes:
            if x not in objc.lower():
                if x not in objectExtra:
                    continue
                
                wdds=objectExtra[x]
                wrds=wdds.split(",")
                
                for wo in wrds:
                    t=re.findall(wo, objc.lower())
                    if len(t)>0:
                        resultType=x
            else:
                resultType=x
         
        
        obj['objecT']=resultType   
        results[d]=obj     

def printResults(results):
    
    fieldnames = ['Date','Object','Price','Location','Category','Object Type','Link']
     
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    fileOutput=os.path.join(pn,'output',"namedEntity.csv")
    
    with open(fileOutput, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()      
    
        for d in results:
            obj=results[d]
            
            res0=obj['date']
            
            date=datetime.strptime(res0, '%b %d, %Y')
            
            res1=obj['object']
            res2=obj['price']
            
            v=str(res2.replace("$","").strip()).replace(',','').strip()
            res2F=float(v)
            res3=obj['location'].split(",")
            
            loc=""
            if len(res3)>1:
                loc=res3[len(res3)-1].strip()
            else:
                loc=res3[0]
            
            if 'Russian Federation' in loc:
                loc="Russia"
            
            if 'Yugoslavia' in loc:
                loc='Serbia'
                
           
            res4=obj['category']
            res5=obj['links']
            
            res6=obj['objecT']
            
            writer.writerow({'Date': str(date),'Object':str(res1),'Price':str(res2F),'Location':str(loc),'Category':str(res4),
                            'Object Type':str(res6), 'Link':str(res5)})
            
def lookAtNewText():
  
    for d in entities:
        lst=entities[d]
        
        print(d+" "+"Length: "+str(len(lst)))
    

    
def run():
#    train_model()
    results=loadData()
    lookAtText(results)
    printResults(results)
    print("Finished")
   
if __name__ == '__main__':
    run()
