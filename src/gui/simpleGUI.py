'''
Simple GUI to run analyses and different components of scraping and NER/dictionary tools.

Created on Jul 30, 2019

@author: Mark Altaweel
'''
import sys
import os
from nltk.tag import StanfordNERTagger
reload(sys)

# handle button events

tP=os.path.abspath(__file__).split("gui")[0]
#jar=os.path.join(tP,"lib","stanford-ner.jar")
#st = StanfordNERTagger('/home/mark/eclipse-workspace/eBayScraper/src/nlp/ner-model.ser.gz',jar,encoding='utf-8')

from appJar import gui 
pF=os.path.abspath(__file__).split('gui')[0]
sys.path.append(pF)
from scraper import scrapeData
from merger import mergeMultipleResults
from merger import mergeMultipleOutputs
from merger import mergeResults
from nlp import nameEntityRecog


'''
Action button to launch options to run, clean, or analyze data
@param button an action button selected
'''
def press(button):
    if button == "Run Scraping":
        scrapeData.runModule()
    elif button=='Remove Duplicate Data':
        mergeMultipleResults.run()
    elif button=='Build NER Model':
        nameEntityRecog.run()
    elif button=='Run NER/dictionary Analysis':
        nameEntityRecog.run()
    elif button=='Clean NER/Dictionary Results':
        mergeMultipleOutputs.run()
    elif button=='Run Spatial Data':
        mergeResults.run()
    else:
        app.stop()
       
# this sets up the GUI
with gui("eBayScraper Application Options", "600x300", bg='orange', font={'size':18}) as app:
    app.label("Welcome to eBayScraper", bg='blue', fg='orange')
    
    app.buttons(["Run Scraping"], press)
    app.buttons(["Remove Duplicate Data"], press)
    app.buttons(["Build NER Model"], press)
    app.buttons(["Run NER/dictionary Analysis"], press)
    app.buttons(["Clean NER/Dictionary Results"], press)
    app.buttons(["Run Spatial Data"], press)
    app.buttons(['Cancel'],press)