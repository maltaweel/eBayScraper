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

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.tag import StanfordNERTagger
from nltk.stem import WordNetLemmatizer

porter=PorterStemmer()
reload(sys)
sys.setdefaultencoding('utf8')
st = StanfordNERTagger('ner-model.ser.gz')
lemmatizer = WordNetLemmatizer()


#spacy.prefer_gpu()
#nlp = spacy.load('en')

objectTypes={'jewellery','vessel','statue','weapon','text','clothing','household','coin','mask','religious','tool','painting','portrait','decoration'}

objectExtra={}

materialType={}

cultures=[]

done=[]


equals={}

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
    
    t=''
    if w.lower() in eqls:
        d=eqls[w]
        d=d.strip()     
        wrds=d.split(",")
        
       
        for wo in wrds:
            if wo == "":
                continue
            
            s=re.findall(wo, doc.lower())
            if len(s)==0:
                t=re.findall(lemmatizer.lemmatize(wo), doc.lower())
            if len(s)>0:
                return w
        
    
    else:
        t=re.findall(w, doc.lower())
        if len(t)==0:
            t=re.findall(lemmatizer.lemmatize(w), doc.lower())
        if len(t)>0:
            return w
   
    return t


def printCantFindType(res1,eqls):
            
    p=st.tag(res1.split())
            
    
    res=''
    for s in p:
        b=s[1]
#        print(b.lower())
            
        if b.lower() in eqls:
            res=b+" | "
               
                                
           
    
                
    return res
    
    
def loadExtraData ():
   
    #This code changes the current directory so relative paths are used
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'inputData','objectExtra.csv')

    
   
    with open(os.path.join(pathway),'rU') as csvfile:
            reader = csv.DictReader(csvfile)

           
            for r in reader:
                
                for rn in r:
                    
                    rt=rn.split(" | ")[0]
                    if rt =='':
                        continue
                    ty=''
                    try:
                        ty=rn.split(" | ")[1]
                        
                        
                    except:
                        print('stop')
                        
                    its=r[rn]
                    
                    if ty in 'objectExtra':
                          
                        xtz=''  
                        
                        if rt in objectExtra:
                            xtz=objectExtra[rt]
                            
                            if its != "":
                                xtz+=","+its  
                            
                        
                        else:
                            if its != "":
                                xtz=rt+","+its
                            else:
                                xtz=rt
                        objectExtra[rt]=xtz
                        
                        if rt not in objectTypes:
                            objectTypes.add(rt)
                        
                    elif ty in 'materialType':
                        
                        xtz=''
                         
                        if rt in materialType:
                            xtz=materialType[rt]
                            
                            if its != '':
                                xtz+=","+its
                            if its == xtz:
                                continue 
                        else:
                            if its != "":
                                xtz=rt+","+its
                            else:
                                xtz=rt
                        materialType[rt]=xtz
                        
                    elif ty in 'cultures':
                       
                        if rt in equals:
                            xtz=equals[rt]
                            if its == xtz:
                                continue
                            if its !="":
                                xtz+=","+its
                            equals[rt]=xtz
                        else:
                            if its !='':
                                equals[rt]=rt+","+its
                            else:
                                equals[rt]=rt
                            if rt not in cultures:
                                cultures.append(rt)
                            
                    
            

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
                        
                        if m=='METAL' and 'bronze age' in org.lower() or m=='METAL' and 'iron age' in org.lower():
                            continue
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
                for w in cultures:
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
            x2=lemmatizer.lemmatize(x)
            if x not in objc.lower() and x2 not in objc.lower():
                if x not in objectExtra:
                    continue
                
                wdds=objectExtra[x]
                wrds=wdds.split(",")
                
                for wo in wrds:
                    if wo == '':
                        continue
                    wo=wo
                    t=re.findall(wo, objc.lower())
                    
                    if len(t)==0:
                        t=re.findall(lemmatizer.lemmatize(wo), objc.lower())

                        
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
                res4=printCantFindType(res1.lower(),equals) 
                
            res4=res4.capitalize()
            res5=obj['links']
            
            res6=obj['objecT']
            
            
            mat=obj['matType']
                   
            if mat=='':
                mat=printCantFindType(res1.lower(),materialType)
                
            
            if res6=='':
                res6=printCantFindType(res1.lower(),objectExtra)
               
                
            
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
