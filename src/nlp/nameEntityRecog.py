'''
Created on Jan 16, 2019

@author: mark
'''

import spacy
import csv
from spacy import displacy
from collections import Counter
import en_core_web_sm
import nltk
import os
nlp = en_core_web_sm.load()

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

def lookAtText(text):
    doc = nlp(text)
    
    print([(X.text, X.label_) for X in doc.ents])
    
if __name__ == '__main__':
   results=loadData()
   
   print("Finished")
