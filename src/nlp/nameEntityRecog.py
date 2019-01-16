'''
Created on Jan 16, 2019

@author: mark
'''

import spacy
import csv
import nltk
import os
import random

spacy.prefer_gpu()
nlp = spacy.load('en')


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
                        date1=objct.split("2019")
                        date2=objct.split("2018")
                        
                        dateKeep=''
                        if len(date1)>1:
                            s1=date1[0].replace("Sold","").strip()
                            dateKeep=s1+" 2019"
                            
                        else:
                            s2=date2[0].replace("Sold","").strip()
                            dateKeep=s2+" 2019"
                        
                        
                        price=row['Price']
                        location=row['Location']
                        link=row['Links']
                        
                        obj['date']=dateKeep
                        obj["object"]=objct
                        obj["price"]=price
                        obj['links']=link
                        obj['location']=location
                        
                        results[objct]=obj
                        
    return results

def lookAtText(results):
    
    keys=results.keys()
    
    for d in results:
        obj=results[d]
        
        objc=obj['object']
        u = unicode(objc, "utf-8")
        
        doc = nlp(u)
    
        print([(X.text, X.label_) for X in doc.ents])

def printResults(results):
    
    fieldnames = ['Object','Price','Location','Links']
     
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    fileOutput=os.path.join(pn,'output',"namedEntity.csv")
    
    with open(fileOutput, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()      
    
        for d in results:
            obj=results[d]
            
            res1=""
            res2=""
            res3=""
            res4=""
            
            writer.writerow({'Object':str(res1),'Price':str(res2),'Location':str(res3),'Links':str(res4)})
    

    
def run():
#    train_model()
    results=loadData()
    lookAtText(results)
   
    print("Finished")
   
if __name__ == '__main__':
    run()
