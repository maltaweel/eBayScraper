'''
Created on Jan 16, 2019

@author: mark
'''

#import spacy
import csv
import nltk
import os
import sys
import re
from datetime import datetime
from boto.mturk import price
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.tag import StanfordNERTagger

porter=PorterStemmer()
reload(sys)
sys.setdefaultencoding('utf8')

#spacy.prefer_gpu()
#nlp = spacy.load('en')

objectTypes={'jewellery','vessel','statue','weapon','text','clothing','household','coin','mask','religious','tool','painting','portrait'}

objectExtra={'weapon':'axe,sword,dager,sheath,sling,arowhead,aroowhead,battle axe,knife,knives,arrow,chariot fitting,point,mace,dagger,projectile,shield,sabre,helmet,arrowhead,spear,military standard',
             'vessel':'pottery,flagon,rhyton,unguentarium,lantern,coffee pot, pot ,plate,chalice,urn,purse,teapot,surma-dani,surma dani,soorma dani,skyphos,ware,cosmetic,pitcher,lamp,kettle,jar,cup,beaker,jug,flaggon,bottle,flask,vessel,bowl,cup,vase,pitcher',
             'statue':'statue,statu,bust,relief,idol,figure,engraving,bust,head fragment,statuette,stone carving,statuete,figurine,plaque,shabti',
             'jewellery':'ring,jewelry,band,amuelt,bangle,pendent,necklace,stone head,glass fish,ear plug,disc,disk,inlay,ornament,medallion,bead,earring,earing,amulet,scarab,scrab,pendant, seal ,signet,bracelet',
             'text':'tablet,inscription,calligraphy,writing,hieroglyphs,graffiti,inscribed,book,manuscript,foundation cone,hieroglyphics',
             'clothing':'brooch,broach,pin,sock,shoe,fibula,gilt mount,cloth,buckle,button,belt',
             'household':'smoking pipe,brick,candlestick,fire striker,strapend,strap end,headrest,furniture,key,dice,altar,spoon,cigarette holder,gaming,nail,box,mosaic,mirror,triptych',
             'coin':'money,denarius,stater,tetradrachm,follis,sceat,sceatta',
             'religious':'cross,crucifix,qoran,quran,deity,sekhmet,ritual,sakhmet,sakhet,baptism,votive,koran,holy,orthodox,buddha,hindu',
             'painting':'paint','portrait':'portrait',
             'tool':'scale,spur,sickle,awl,quern,wheel,strap fitting,walking stick,adze,stamp,razor,whistle,pestle,comb,mortar,hook,knife,knives,chisel,needle,lithic,obsidian,chisle,hammer,spindle,weight,medical'}

words={'roman','byzantine','scythian','islamic','egyptian','greek','viking','revolutionary', 'renaissance',
       'khazar','mogul','bronze age','iron age','russian','celt',
       'america','pre-historic','china','japan','buddhist','near east','mongul','indus','central asia'}

done=[]


equals={'celt':'seltic','egytpian':'egypt', 
        'america':'columbian,maya,aztec,native american,pre columbian,mexico,pre-columbian,indian',
        'islamic':'koran,andalus,qajar,quran,khazar,sulimani','buddhist':'buddhist,bamiyan',
        'roman':'rome,romano', 'greek':'cypriot,athena,greco,mycenaean,macedonia,byzantine',
         'russian':'russiam','indus':'indo,gandhara','pre-historic':'neolithic,pre historic,stone age,mesolithic,chalcolithic,paleolithic,palaeolithic',
         'near east':'near east,yemen,arabic,yamani,yemani,persia,ottoman,persian,judaea,holy land,phoenician,mesopotamia,middle east,israel,canaanite,crusader',
         'egyptian':'pharao,pharaoh,ptolemaic','viking':'saxon,norse,nordic',
         'china':'chinese','renaissance':'baroque,italian',
         'japan':'japanese','central asia': 'central asia,scythian,scythian,sythian,khanate,bactria,kazar,khazar',
         'cambodia':'cambodian','khmer':'cambodian','thailand':'thai','thai': 'thai'}

entities={}

def stemSentence(sentence):
    token_words=word_tokenize(sentence.decode('utf-8'))
    token_words
    stem_sentence=[]
    for word in token_words:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)

def findWholeWord(w,doc):
    
    if w.lower() in equals:
        d=equals[w]
        d=d.strip()     
        wrds=d.split(",")
        
        for wo in wrds:
            if wo == "":
                continue
            t=re.findall(wo, doc.lower())
            if len(t)>0:
                return t
        
    
   
    t=re.findall(w, doc.lower())
    
   
    return t

def printCantFindType(cantFind):
    fieldnames = ['Date','Object','Price','Location','Category','Object Type','Link']
     
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    fileOutput=os.path.join(pn,'output',"cantFindEntity.csv")
    
    
    with open(fileOutput, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()      
    
        for obj in cantFind:
            
            res0=obj['date']
            
            date=datetime.strptime(res0, '%b %d, %Y')
            st = StanfordNERTagger('ner-model.ser.gz')
           
            res1=obj['object']
            res2=obj['price']
            
            p=st.tag(res1.split())
            print(p)
            
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
            res4=res4.capitalize()
            res5=obj['links']
            
            res6=obj['objecT']
            
            if res6=='':
                res6='?'
            
            
            writer.writerow({'Date': str(date),'Object':str(res1),'Price':str(res2F),'Location':str(loc),'Category':str(res4),
                            'Object Type':str(res6), 'Link':str(res5)})
    
    
def loadExtraData ():
   
    #This code changes the current directory so relative paths are used
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'inputData','objectExtra.csv')

    
   
    with open(os.path.join(pathway),'rU') as csvfile:
            reader = csv.DictReader(csvfile)

            for objT in objectTypes:
                if objT not in objectExtra:
                    continue
                
                objTy=objectExtra.get(objT)
                
                if objTy is None or objTy ==' ':
                    continue
                
                tys=objTy.split(",")
                
                
                for read in reader:
                    r=read[objT]
                    
                    if r not in tys:
                        tys.append(r)
                    
                stR=""
                for r in tys:
                    stR+=r+","  
                    
                    objectExtra[objT]=stR
                    
            
            for w in words:
                if w not in equals:
                    continue
                wrds=equals[w]
                
                if wrds is None:
                    continue
                
                tys=wrds.split(",")
                
               
                
                for read in reader:
                    r=read[w]
                    
                    if r not in tys:
                        tys.append(r)
                    
                stR=""
                
                
                for r in tys:
                    stR+=r+','  
                
                    equals[w]=stR
                
'''                        
def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    newSent = nltk.pos_tag(sent)
    
    return newSent
'''

def loadData():
    #This code changes the current directory so relative paths are used
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'data')

    results={}
    
    
        
    for fil in os.listdir(pathway):
        with open(os.path.join(pathway,fil),'rU') as csvfile:
            reader = csv.DictReader(csvfile)
                
                
            i=0
            for row in reader:
                obj={}
                org=row['Object']
                price=row['Price']
                date1=org.split("2019")
                date2=org.split("2018")
                
                for word in words:
                    if i==0:
                        i+=1
                    else:
                          
                        
                      # objct=stemSentence(org)
                        objct=org
                        objct.replace(",","")
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
                        
                        cat=''
                        if obj.has_key('category'):
                            cat=obj['category']
                            obj['category']=word+" "+cat
                        
                        else:
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
                    if wo == '':
                        continue
                    wo=wo
                    t=re.findall(wo, objc.lower())
                    if len(t)>0:
                        if x in resultType:
                            continue
                        resultType+=x+" "
            else:
                resultType=x
         
        
        obj['objecT']=resultType   
        results[d]=obj     
            
def printResults(results):
    
    fieldnames = ['Date','Object','Price','Location','Category','Object Type','Link']
     
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    fileOutput=os.path.join(pn,'output',"namedEntity.csv")
    cantFind=[]
    
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
            res4=res4.capitalize()
            res5=obj['links']
            
            res6=obj['objecT']
            
            if res6=='':
                res6='?'
                cantFind.append(obj)
            
            writer.writerow({'Date': str(date),'Object':str(res1.decode('utf-8')),'Price':str(res2F),'Location':str(loc.decode('utf-8')),'Category':str(res4.decode('utf-8')),
                            'Object Type':str(res6.decode('utf-8')), 'Link':str(res5.decode('utf-8'))})
    
    printCantFindType(cantFind)  
     
def lookAtNewText():
  
    for d in entities:
        lst=entities[d]
        
        print(d+" "+"Length: "+str(len(lst)))
    
    
def run():
#    train_model()
    loadExtraData()
    results=loadData()
    lookAtText(results)
    printResults(results)
    print("Finished")
   
if __name__ == '__main__':
    run()
