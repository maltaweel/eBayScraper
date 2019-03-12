'''
Created on Mar 12, 2019

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
st = StanfordNERTagger('ner-model.ser.gz')

#spacy.prefer_gpu()
#nlp = spacy.load('en')

objectTypes={'jewellery','vessel','statue','weapon','text','clothing','household','coin','mask','religious','tool','painting','portrait','decoration'}

objectExtra={'weapon':'axe,sword,cuiras,dager,sheath,military fitting,sling,armour,arowhead,aroowhead,battle axe,knife,knives,arrow,chariot fitting,point,mace,dagger,projectile,shield,sabre,helmet,arrowhead,spear,military standard',
             'vessel':'pottery,trulla,kylix,flagon,rhyton,unguentarium,lantern,coffee pot, pot ,plate,chalice,urn,purse,teapot,surma-dani,surma dani,soorma dani,skyphos,ware,cosmetic,pitcher,lamp,kettle,jar,cup,beaker,jug,flaggon,bottle,flask,vessel,bowl,cup,vase,pitcher',
             'statue':'statue,faience cat,statu,bust,relief,idol,figure,engraving,bust,head fragment,statuette,stone carving,statuete,figurine,plaque,shabti,ushabti',
             'jewellery':'ring,diadem,jewelry,band,amuelt,bangle,pendent,necklace,stone head,glass fish,ear plug,disc,disk,inlay,ornament,medallion,bead,earring,earing,amulet,scarab,scrab,pendant, seal ,signet,bracelet',
             'text':'tablet,inscription,calligraphy,papyrus,writing,hieroglyphs,graffiti,inscribed,book,manuscript,foundation cone,hieroglyphics',
             'clothing':'brooch,broach,pin,sock,shoe,fibula,gilt cloth,buckle,button,belt',
             'household':'smoking pipe,brick,candlestick,fire striker,strapend,strap end,headrest,furniture,key,dice,altar,spoon,cigarette holder,gaming,nail,box,mosaic,mirror,triptych',
             'coin':'money,denarius,stater,tetradrachm,follis,sceat,sceatta',
             'religious':'cross,crucifix,thor,qoran,anubis,quran,deity,horus,isis,sekhmet,hermes,ritual,sakhmet,sakhet,baptism,votive,koran,holy,orthodox,buddha,hindu',
             'painting':'paint','portrait':'portrait',
             'tool':'scale,spur,fire starter,stylus,lantern,sickle,awl,hammer,quern,mount,wheel,strap fitting,harness,walking stick,adze,stamp,razor,whistle,pestle,comb,mortar,hook,knife,knives,chisel,needle,lithic,obsidian,chisle,spindle,weight,medical'}

materialType={'terracotta':'terracotta,clay,glaze,faience','metal':'metal,bronze,silver,gold,lead,tin,iron,copper','glass':'glass,vitrified',
              'stone':'agate,carnelian,flint,lapis,lazuli,stone'}

words={'roman','byzantine','scythian','islamic','egyptian','greek','viking','revolutionary', 'renaissance',
       'khazar','mogul','bronze age','iron age','russian','celt','africa'
       'america','pre-historic','china','japan','buddhist','near east','mongul','indus','central asia'}

done=[]


equals={'celt':'seltic','egytpian':'egypt', 
        'america':'columbian,maya,aztec,native american,pre columbian,mexico,pre-columbian,indian',
        'islamic':'koran,andalus,qajar,quran,khazar,sulimani','buddhist':'buddhist,bamiyan',
        'roman':'rome,romano', 'greek':'cypriot,athena,greco,mycenaean,macedonia,byzantine',
         'russian':'russiam','indus':'indo,gandhara','pre-historic':'neolithic,pre historic,stone age,mesolithic,chalcolithic,paleolithic,palaeolithic',
         'near east':'near east,yemen,bedouin,arabic,yamani,yemani,persia,ottoman,persian,judaea,holy land,phoenician,mesopotamia,middle east,israel,canaanite,crusader',
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

def findWholeWord(w,doc, eqls):
    
    if w.lower() in eqls:
        d=eqls[w]
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


def printCantFindType(obj):
            
    p=st.tag(obj.split())
            
    return p
    
def loadData():
    #This code changes the current directory so relative paths are used
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'data')

    results={}
    
    
        
    for fil in os.listdir(pathway):
        with open(os.path.join(pathway,fil),'rU') as csvfile:
            reader = csv.DictReader(csvfile)
                
                
           
            for row in reader:
                obj={}
                org=row['Object']
                    
                price=row['Price']
                date1=org.split("2019")
                date2=org.split("2018")
                
                objct=org
                objct.replace(",","")
                
                p=printCantFindType(objct)
                
                for s in p:
                    tm=str(s[1]).lower()
                    if tm in objectTypes:
                        obj['objectT']=s[1]
                    elif tm in materialType:
                        obj['matType']=s[1]
                    elif tm in words:
                        obj['category']=s[1]
                
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
                
                results[objct]=obj
                        
    return results

def lookAtText(obj):
    
   
        objc=obj['object']
        
        resultType='?'
        '''
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
                        resultType+=x+" | "
         
        '''
        obj['objecT']=resultType   
        return obj     
            
def printResults(results):
    
    fieldnames = ['Date','Object','Price','Location','Category','Object Type','Material','Link']
     
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
            
            if res4=='':
                res4='?'
                
            res4=res4.capitalize()
            res5=obj['links']
            
            res6=obj['objecT']
            
            mat=obj['matType']
                   
            if mat=='':
                mat='?'
                
            
            if res6=='':
                res6='?'
                
            
            writer.writerow({'Date': str(date),'Object':str(res1.decode('utf-8')),'Price':str(res2F),'Location':str(loc.decode('utf-8')),'Category':str(res4.decode('utf-8')),
                            'Object Type':str(res6.decode('utf-8')),'Material':str(mat),'Link':str(res5.decode('utf-8'))})
    
     
def lookAtNewText():
  
    for d in entities:
        lst=entities[d]
        
        print(d+" "+"Length: "+str(len(lst)))
   


def run():

    results=loadData()
    printResults(results)
    print("Finished")
   
if __name__ == '__main__':
    run()