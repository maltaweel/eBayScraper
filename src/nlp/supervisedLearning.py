'''
Created on Feb 25, 2019

@author: mark
'''
import pandas as pd
import numpy as np # linear algebra
import seaborn as sns
import matplotlib.pyplot as plt
import base64
import string
import re
import os

from collections import Counter
from nltk.corpus import stopwords
stopwords = stopwords.words('english', 2)


pn=os.path.abspath(__file__)
pn=pn.split("src")[0]
pathway=os.path.join(pn,'inputData','namedEntity.csv')
df = pd.read_csv(pathway)
df.head()

df.shape
df.isnull().sum()