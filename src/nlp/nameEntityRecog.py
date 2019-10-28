'''
Module that performs Named Entity Recognition and dictionary searches on input terms.
The modul takes an input file(s) from the data folder and then returns an output in the output folder (called namedEntity.csv)

Created on Jan 16, 2019

@author: 
'''

#import spacy
import csv
import nltk
import os
import sys
import re
from datetime import datetime

tP=os.path.abspath(__file__).split("src")[0]
pathJ=os.path.join(tP,"lib","stanford-ner.jar")
sys.path.append(pathJ)

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.tag import StanfordNERTagger
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

from spellchecker import SpellChecker
spell = SpellChecker()


porter=PorterStemmer()
reload(sys)
sys.setdefaultencoding('utf8')


lemmatizer = WordNetLemmatizer()

#some default inputs included in this list of object types. Others can be added.
objectTypes={'jewellery','vessel','statue','weapon','text','clothing','household','coin','mask','religious','tool','painting','portrait','decoration'}

#dictionary used to reference a type of object with other terms affiliated with the object categorisation
objectExtra={}

#material references associated with a given category of material (e.g., bone, wood, etc.)
materialType={}

#list of cultures added and used in categorisation
cultures=[]

#list to keep track of redundant material that can be removed
done=[]

#dictionary of cultures that includes multiple references for the same cultural categorisation used 
#(e.g., Ottoman, Phoenician, Hittite being Near East cultures)
equals={}

#entities={}

'''
Method to check spelling of an English word
@param word- a word to check spelling for, returing the most likely spelling

@return the corrected or 'best' spelling.
'''
def spelling(word):
    
    return spell.correction(word)
   
''''
Method to parse a given sentence and then commence spell check, with the sentence then being reformed.

@param sentence- the sentence to check
@return sentence- the spell corrected sentence
'''
def spellCheck(sentence):
    
    #below code will tokenize the sentence to terms
    #then check terms for their spelling
    #the sentence is then put back together
    try:
        b = TextBlob(sentence)
        lang=b.detect_language()
        if lang!='en':
            return sentence
        sentence=sentence.replace("-"," ")
        token_words=word_tokenize(sentence.decode('utf-8'))
        token_words
        stem_sentence=[]
        for word in token_words:
            stem_sentence.append(spelling(word))
            stem_sentence.append(" ")
        return "".join(stem_sentence)
    
    except:
        return sentence

'''
Method to find a word in a text using regular expression searches
@param w- the cateogory term to search (e.g., Roman, Celtic, European, etc.)
@param doc- the document to search, which is the text description
@param eqls- the dictionary containing the terms associated with a category term (e.g., Celtic is also Celt, Celts, Selts)

@return s- the number of terms found
@return t- the number of terms found
'''
def findWholeWord(w,doc, eqls):
    
    
    t=''
    if w.lower() in eqls:
        d=eqls[w]
        d=d.strip()     
        wrds=d.split(",")
        
       
        for wo in wrds:
            if wo == "":
                continue
            
            #regular expression term search
            s=re.findall(wo.lower(), doc.lower())
            if len(s)==0:
                t=re.findall(lemmatizer.lemmatize(wo.lower()), doc.lower())
                if len(t)>0:
                    return t
            else:
                return s
        
    ''' 
    else:
        t=re.findall(w.lower(), doc.lower())
        if len(t)==0:
            t=re.findall(lemmatizer.lemmatize(w.lower()), doc.lower())
            if len(t)>0:
                return t
        
        else:
            return t
    '''
    return t


'''
Method where the main NER model is used. Here the Standford CRF classifier is used.
@param obj- the dictionary containing information about the object entry, including information such as the material type and object type
@param res1- the description of the cultural object
'''
def printCantFindType(obj,res1):
    #this applies the NER model      
    tP=os.path.abspath(__file__).split("src")[0]
    jar=os.path.join(tP,"lib","stanford-ner.jar")
    pathGZ=os.path.abspath(__file__).split("nameEntityRecog.py")[0]
    st = StanfordNERTagger(os.path.join(pathGZ,'ner-model.ser.gz'),jar,encoding='utf-8') 
    p=st.tag(res1.split())
            
    #then go through the results, getting the second output which fits one of three categories
    #the three categories relate to object type, culture, and material of object
    listT=[]
    for s in p:
        b=s[1]
#        print(b.lower())
        
        if b.lower() in listT:
            continue
        
        if b.lower() in equals:
            term=obj['category']
            if b.lower() in term:
                continue
            
            obj['category']=term+b.lower()+" | "
        
        elif b.lower() in objectTypes:
            obJT=obj['objectT']
            if b.lower() in obJT:
                continue
            
            obj['objectT']=obJT+b.lower()+" | "
        
        elif b.lower() in materialType:
            matT=obj['matType']
            if b.lower() in matT:
                continue
            obj['matType']=matT+b.lower()+" | "
                                
        listT.append(b)
    
                
'''
Method that loads search terms from a dictionary on the type of cultural object, type of cultures, and material of the object's composition from
an input file in the inputData folder. The terms are affiliated with given categories (e.g., seltic is part of the category term celtic).
'''
def loadExtraData ():
   
    #This code changes the current directory so relative paths are used
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'inputData','objectExtra.csv')

    #the below steps simply match the type of object, cultural type, and material of objects    
    try:
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
    except IOError:
        print "Could not read file:", csvfile
                    
            
'''
The is the method that is called and obtains data from the input eBay data. The NER is first called and then a dictionary search.
The results are also printed to the namedEntity.csv file in the output folder
'''
def loadData():
    #This code changes the current directory so relative paths are used
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'data')
    
    fieldnames = ['Date','Object','Price','Location','Category','Object Type','Material','Seller','Link']
    
    fileOutput=os.path.join(pn,'output',"namedEntity.csv")
    
    #open the output file so output can be written while applying the methods
    with open(fileOutput, 'wb',buffering=0) as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader() 
        for fil in os.listdir(pathway):
            with open(os.path.join(pathway,fil),'rU') as csvfile:
                reader = csv.DictReader(csvfile)
 
                for row in reader:
                    
                    #get some of the basic data from the scraped file, including description, sale price (in dollars) and date info.
                    obj={}
                    org=row['Object']
                    price=row['Price']
                    date1=org.split("2019")
                    date2=org.split("2018")
                    
                    #spell check launched here
                    org=spellCheck(org)
                    objct=org
                    objct.replace(",","")
                    totalP=objct+' '+price
                    
                            
                    if totalP in done:
                        continue
                
#                    done.append(totalP)

                    dateKeep=''
                            
                    if len(date1)>1:
                        s1=date1[0].replace("Sold","").strip()
                        dateKeep=s1+" 2019"
                            
                    else:
                        s2=date2[0].replace("Sold","").strip()
                        dateKeep=s2+" 2018"
                        
                    date=datetime.strptime(dateKeep, '%b %d, %Y')    
                        
                    location=row['Location']
                    link=row['Link']
                        
                    obj['date']=dateKeep
                    obj["object"]=objct
                        
                    #obj=lookAtText(obj)
                        
                    #put some of the scraped data as part of the output that will go in namedEntity.csv  
                    obj["price"]=price
                    obj['links']=link
                    obj['location']=location
                    obj['matType']=''
                    obj['category']=''
                    obj['objectT']=''
                    
                    mat=''
                    oT=''
                    cat=''
                    
                    #this does the method for NER
                    printCantFindType(obj,objct)
                    
                    #this does the dictionary searches
                    for w in materialType:
                        mat=obj['matType']
                        if w.lower() in mat.lower():
                            continue
                        m=findWholeWord(w,org.lower(),materialType)
                        if len(m)>0:
                            obj['matType']+=w+" | "
                
                    if obj['matType']=="":
                        obj['matType']='?'
                
                    for o in objectTypes:
                        oT=obj['objectT']
                        if o.lower() in oT.lower():
                            continue
                        mn=findWholeWord(o,org.lower(),objectExtra)
                        if len(mn)>0:
                            obj['objectT']+=o+" | "
                
                    if obj['objectT']=="":
                        obj['objectT']='?'
                        
                    for c in cultures:
                        cat=obj['category']
                        if c.lower() in cat:
                            continue
                        t=findWholeWord(c, objct.lower(), equals)
                    
                        if len(t) > 0:
                            obj['category']+=c+" | "
                       
                    if obj['category']=='':
                        obj['category']='?'
                    
                    loc=''
                    res3=obj['location'].split(",")
                    if len(location)>1:
                        loc=res3[len(res3)-1].strip()
                    else:
                        loc=res3[0]
            
                    if 'Russian Federation' in location:
                        loc="Russia"
            
                    if 'Yugoslavia' in location:
                        loc='Serbia'
                    
                    v=str(price.replace("$","").strip()).replace(',','').strip()
                    res2F=float(v)
                    
                    #row['Seller']
                    writer.writerow({'Date': str(date),'Object':str(objct.decode('utf-8')),
                            'Price':str(res2F),'Location':str(loc.decode('utf-8')),'Category':str(obj['category'].decode('utf-8')),
                            'Object Type':str(obj['objectT'].decode('utf-8')),
                            'Material':str(obj['matType']),'Seller':str(''),'Link':str(link.decode('utf-8'))})
'''
Method to run the module and launch the analysis
'''                    
def run():
    
    #first load any data we need for dictionary searches
    loadExtraData()
    
    #launch the analysis that will do NER and dictionary searches
    loadData()

    print("Finished")
   
if __name__ == '__main__':
    run()
