'''
Module used to compare images to each other and rate based on similarity.

Created on Jul 3, 2019

@author: Mark Altaweel
'''
import csv
from PIL import Image
import urllib2
import numpy as np
import os
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.models import Model
import numpy as np
from os import listdir, walk
from os.path import isfile, join
import itertools
import cv2

from sklearn.model_selection import train_test_split

def getAllFilesInDirectory(directoryPath):
    return [(directoryPath + "/" + f) for f in listdir(directoryPath) if isfile(join(directoryPath, f))]

def predict(img_path, model):
    
    im = Image.open(urllib2.urlopen(img_path))
    im = im.resize((224, 224))
#   img= cv2.resize(im, (224,224),3)
    
#   img = image.load_img(im, target_size=(224, 224))
#    x = image.img_to_array(img)
    x = image.img_to_array(im)
    
    x = np.expand_dims(x, axis=0)

    x = preprocess_input(x)
    return model.predict(x)

def findDifference(f1, f2):
    return np.linalg.norm(f1-f2)

'''
def findDifferences(feature_vectors):
    similar: dict = {}
    keys = [k for k,v in feature_vectors.items()]
    min = {}
    for k in keys:
        min[k] = 10000000
    possible_combinations=list(itertools.combinations(keys, 2))
    for k,v in possible_combinations:
       diff=findDifference(feature_vectors[k],feature_vectors[v])
       if(diff < min[k]):
           min[k] = diff
           similar[k] = v
           min[v] = diff
           similar[v] = k
    return similar
'''

def findDifferences(feature_vectors1,feature_vectors2):
    similar = {}
    keys={}#
    keys2={}
    min={}
    min2 = {}
#   for k in feature_vectors1.items():
#        keys[k]=k

    keys = [k for k,v in feature_vectors1.items()]
    
    for k in keys:
        min[k] = 10000000
        
    possible_combinations=list(itertools.combinations(keys, 2))
    
    
    keys2 = [kk for kk,v in feature_vectors2.items()]
#    for k in feature_vectors2.items():
#        keys2[k]=k
        
   
    for kk in keys2:
        min2[kk] = 10000000
        
    possible_combinations2=list(itertools.combinations(keys2, 2))
    
    for k, v in possible_combinations:
           for l, w in possible_combinations2:
               diff=findDifference(feature_vectors1[k],feature_vectors2[w])
               if(diff < min[k]):
                   min[k] = diff
                   similar[k] = w
                   min[w] = diff
                   similar[w] = k
               
    return similar 

def driver():
    feature_vectors_eby = {}
    feature_vectors_pas = {}
    
    model = ResNet50(weights='imagenet')
    imgsE=images("scrapedOutput.csv")
    imgsPAS=images("pasSiteOutput.csv")
    for img_pathE in imgsE:
        feature_vectors_eby[img_pathE] = predict(img_pathE,model)[0]
    for img_pathPAS in imgsPAS:
        feature_vectors_pas[img_pathPAS] = predict(img_pathPAS,model)[0]
    results=findDifferences(feature_vectors_eby,feature_vectors_pas)
    for k,v in results.items():
        print(k +" is most similar to: "+ v)    
   # print('Predicted:', decode_predictions(preds, top=3)[0])
    
def path():
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'output')
 
    return pathway

 
def images(fil):
    pathway=os.path.join(path(),fil)
    
    with open(pathway,'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        images=[]
        
        for r in reader:
            images.append(r['Image'])
    
    return images
    
    
'''
The main to launch this module
'''
if __name__ == '__main__':
    driver()