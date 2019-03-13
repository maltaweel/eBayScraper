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
st = StanfordNERTagger('ner-model.ser.gz')

#spacy.prefer_gpu()
#nlp = spacy.load('en')

objectTypes={'jewellery','vessel','statue','weapon','text','clothing','household','coin','mask','religious','tool','painting','portrait','decoration'}

objectExtra={'weapon':'axe,sword,cuiras,dager,arow,sheath,military fitting,lorica,sling,armour,arowhead,aroowhead,battle axe,knife,knives,arrow,chariot fitting,point,mace,dagger,projectile,shield,sabre,helmet,arrowhead,spear,military standard',
             'vessel':'pottery,olpe,trulla,kylix,flagon,rhyton,unguentarium,lantern,coffee pot, pot , plate ,chalice,urn,purse,teapot,surma-dani,surma dani,soorma dani,skyphos,ware,cosmetic,pitcher,lamp,kettle,jar,cup,beaker,jug,flaggon,bottle,flask,vessel,bowl,cup,vase,pitcher',
             'statue':'statue,statuette,faience cat,statu,bust,relief,idol,figure,engraving,bust,head fragment,stone carving,statuete,figurine,plaque,shabti,ushabti',
             'jewellery':'ring,diadem,jewelry,band,amuelt,bangle,pendent,necklace,stone head,glass fish,ear plug,disc,disk,inlay,ornament,medallion,bead,earring,earing,amulet,scarab,scrab,pendant, seal ,signet,bracelet',
             'text':'tablet,inscription,calligraphy,papyrus,writing,hieroglyphs,graffiti,inscribed,book,manuscript,foundation cone,hieroglyphic',
             'clothing':'brooch,broach,pin,sock,shoe,fibula,gilt cloth,buckle,button,belt',
             'household':'smoking pipe,brick,candlestick,strapend,strap end,headrest,furniture,key,dice,altar,spoon,cigarette holder,gaming,nail,box,mosaic,mirror,triptych',
             'coin':'money,denarius,stater,tetradrachm,follis,sceat,sceatta',
             'religious':'cross,crucifix,thor,qoran,anubis,quran,deity,horus,isis,sekhmet,hermes,ritual,sakhmet,sakhet,baptism,votive,koran,holy,orthodox,buddha,hindu',
             'painting':'paint','portrait':'portrait','decoration':'ornament','decoration'
             'tool':'scale,spur,fire starter,fire striker,stylus,lantern,sickle,awl,quern,mount,wheel,strap fitting,harness,walking stick,adze,stamp,razor,whistle,pestle,comb,mortar,hook,knife,knives,chisel,needle,lithic,obsidian,chisle,spindle,weight,medical'}

materialType={'terracotta':'terracotta,clay,glaze,faience','metal':'metal,bronze,silver,gold,lead,tin,iron,copper','glass':'glass,vitrified',
              'stone':'agate,carnelian,flint,lapis,lazuli,stone','wood':'wood'}

words={'roman','byzantine','islamic','egyptian','greek','viking','revolutionary', 'renaissance',
       'khazar','mogul','bronze age','iron age','medieval','russian','celt','africa'
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


def printCantFindType(res1,obj,res4,eqls):
            
    p=st.tag(res1.split())
            
    
 
    for s in p:
        b=s[1]
#        print(b.lower())
            
        if res4!='':
            tx=''
            if b.lower() in objectExtra:
                tx+=b+" | "
            obj['objecT']=tx
    
        else:
            res4=''
            if b.lower() in eqls:
                res4+=b+" | "
               
                                
           
    
                
    return obj, res4
    
    
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
                
          
            for row in reader:
                obj={}
                org=row['Object']
                price=row['Price']
                date1=org.split("2019")
                date2=org.split("2018")
                
                mat=''
                for w in materialType:
                    m=findWholeWord(w,org.lower(),materialType)
                    if len(m)>0:
                        mat+=w+" | "
                
                obj['matType']=mat
                
                          
                # objct=stemSentence(org)
                objct=org
                objct.replace(",","")
                totalP=objct+' '+price
                    
                            
                if totalP in done:
                    continue
                
                done.append(totalP)

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
                        
                obj=lookAtText(obj)
                        
                        
                obj["price"]=price
                obj['links']=link
                obj['location']=location
                obj['category']='' 
                for w in words:
                    t=findWholeWord(w, objct, equals)
                    
                    if len(t) > 0:
                        cat=''
                        if obj.has_key('category'):
                            cat=obj['category']
                            obj['category']=w+" | "+cat
                        
                        else:
                            obj['category']=w
                    else:
                        continue
                
                if obj['category']=='':
                    obj['category']='?'
                    
                results[objct]=obj
                        
    return results

def lookAtText(obj):
    
   
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
                        resultType+=x+" | "
            
            else:
                resultType+=x+" | "
        
        if resultType=='':
            resultType='?'
            
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
                obj, res4=printCantFindType(res1,obj,res4,equals) 
                
            res4=res4.capitalize()
            res5=obj['links']
            
            res6=obj['objecT']
            
            
            mat=obj['matType']
                   
            if mat=='':
                obj, mat=printCantFindType(res1.lower(),obj,'',materialType)
                
            
            if res6=='':
                obj, res4=printCantFindType(res1,obj,res4,objectExtra)
                res6=obj['objecT']
                
            
            writer.writerow({'Date': str(date),'Object':str(res1.decode('utf-8')),'Price':str(res2F),'Location':str(loc.decode('utf-8')),'Category':str(res4.decode('utf-8')),
                            'Object Type':str(res6.decode('utf-8')),'Material':str(mat),'Link':str(res5.decode('utf-8'))})
    
     
def lookAtNewText():
  
    for d in entities:
        lst=entities[d]
        
        print(d+" "+"Length: "+str(len(lst)))
   


def run():
#    train_model()
    loadExtraData()
    results=loadData()
 #  lookAtText(results)
    printResults(results)
    print("Finished")
   
if __name__ == '__main__':
    run()
