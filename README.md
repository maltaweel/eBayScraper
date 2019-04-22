# eBayScraper
<b>Guide to eBayScraper and NERProject</b>

This eBayScraper tool, a Python 2.7+ tool, performs both web scraping and named entity recognition (NER) analysis of eBay sales data on antiquities. The NERProject,  a Java 8 project included as a sub-tool and part of eBayScraper, provides a way to create a supervised classification using conditional random field (CRF). The output of this tool is a classification that is used in the NER analysis within eBayScraper. The following provides a high-level overview of the tools provided as well as more detailed instructions on the contents of the tool.

<b>Required Libraries</b>

<i>Python</i>
The following libraries are used in eBayScraper and are required, including possibly newer versions of the listed libraries.

Python 2.7+
NLTK 3.4
Beautiful Soup 4.4
ebaysdk 2.1.5 (used only for eBayAPI in /src/scraper/ folder)
pysal 2.0
dbfpy 2.0
SpellChecker 0.4
TextBlob 0.15.2
ctypes 1.0.2

<i>Java</i>
The following libraries are used in NERProject and are required, including possibly newer versions of the listed libraries.

Java 8
Stanford CoreNLP 3.9.2:  https://stanfordnlp.github.io/CoreNLP/download.html (see instructions; the lib folder in NERProject has Java libraries needed)

High-Level Overview

<i>eBayScraper</i>

1. src/merger

Modules that merge different scraped data (mergeMultipleOutputs.py and mergeMultipleResults.py). The module mergeMultipleOutputs.py merges the outputs of the NER method, while mergeMultipleResults.py merges scraped data. The mergeResults.py integrates the NER/dictionary results with associated countries where items were sold, providing a country-level spatial dataset of the NER/dictionary results. The spatial dataset provides information on cultures, materials of objects, and general types of objects sold in countries and the dollar value of those sales. 

2. src/nlp

Only module here is nameEntityRecog.py, which applies the named entity recognition technique using the CRF outputs from NERProject. The output is ner-model.ser.gz, located in the nlp folder. In addition, nameEntityRecog.py conducts dictionary regular expression searches, see inputData folder, as well as spell checks on descriptions. 

3. src/scraper

The ebayAPI.py is not currently used but it can be applied to directly integrate with the eBay API platform created by eBay. The scrapeData.py is used to scrape data applying the Beautiful Soup library.

4. src/test

The memoryTest.py module is used to test memory availability and allocation in the applied device. The randomSelector.py is used to produce random output from the NER/dictionary results that are applied in memory-recall or other information retrieval tests. 

5. data

The folder that contains the raw scraped data that will be used in the NER model and dictionary analysis done in src/nlp/nameEntityRecog.py. The data files are .csv files that contain object descriptions, dates of when an eBay item was sold (in the description), the value of the sale, the location of the seller, and the link of the object.

6. images

Not used currently but could be a location for scraped images from eBay used for analysis.

7. inputData

The folder used for dictionary (i.e., regular express) searches in the NER/dictionary model.

8. output

The output folder used for outputting analysis results in the NER/dictionary model and merger outputs. The file namedEntityTotal.csv is the merged scraped data file, while namedEntityMerged.csv is the merged output of the NER/dictionary results.

9. shp

This folder contains a shapefile used to store data about different countries in the categories anlaysed for the NER results. The shapefile integrates NER/dictionary analysis data, using src/merger/mergeResults.py, to enable visualization of the results based on country. The data provide a dollar value of antiquities found in different countries as well as type of antiquities/cultural objects, the material in which these objects are made from, and the cultures in which they are associated. 

10. totalData

Folder used to place files from scarping and/or NER/dictionary analysis outputs so that they can be merged into one data file. 

<i>NERProject</i>

1. src/ner

The folder contains two Java objects, which are NERDemo.java and RunTrainer.java respectively. NERDemo.java is an example NER project from the Stanford team that is included here as a demonstration on how to use NER. The RunTrainer.java is used for creating the ner-model.ser.gz file, which is used in the Python eBayScraper NER analysis. The properties.txt is used as a property file applied in RunTrainer.java and is based on requirements from the Stanford tool.

2. bin/ner

The bin folder for Java classes.

3. classifiers

Classifier libraries from the Stanford NLP group.

4. data

Data files used in NERProject/src/ner/RunTrainer.java. The file findEntity.csv is a demo file that demonstrates how terms are parsed and classified using the CRF classifier. The namedEntity.txt file is use for training and creating the CRF model, which, when created, is called ner-model.ser.gz.

5. doc

The Java doc files which provide documentation and explanation of the Java utilised in the project folder.

6. lib

The Java libraries used from the Stanford CoreNLP tool.

 

