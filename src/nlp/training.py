'''
Created on Jan 16, 2019

@author: mark
'''
import spacy
import random

spacy.prefer_gpu()
nlp = spacy.load('en')


def train_model():
    TRAIN_DATA = [
     ("Roman blew through $1 million a week", {'entities': [(0, 5, 'NORP')]}),
     ("Celtic Nordic Antique Stone  Effigy Figure Of A Man Viking King? No Reserve", {'entities': [(0, 6, "NORP")]}),
     ('BYZANTINE LEAD BROCH PEDANT WITH GREEN AND WHITE BEADS',{'entities': [(0, 9, "NORP")]}),
     ('Egyptian',{'entities': [(0, 9, "NORP")]}),
     ('VIKING BRONZE HANGER WITH TWO HOOKS',{'entities': [(0, 6, "NORP")]}), 
     ('Meotian sword. Meoty. 4th century. Very good condition. Length 70 cm.',{'entities': [(0,7, "NORP")]}), 
     ('PHOENICIAN GLASS FACE',{'entities': [(0,10, "NORP")]}),
     ('GREEK STATUE',{'entities':[(0,5, "NORP")]}),
     ('CHRISTIAN BILLON RING',{'entities':[(0,9, "NORP")]})
     ]
      


    optimizer = nlp.begin_training()
    
    for i in range(20):
        random.shuffle(TRAIN_DATA)
        for text, annotations in TRAIN_DATA:
            nlp.update([unicode(text,'utf-8')], [annotations], sgd=optimizer)
            
            
    nlp.to_disk('/model')

train_model()
print("Finished")