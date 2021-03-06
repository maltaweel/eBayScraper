# eBayScraper
<b>Guide to eBayScraper and NERProject</b>

This eBayScraper tool, an originally Python 2.7+ tool, performs both web scraping and named entity recognition (NER) analysis of eBay sales data on antiquities/cultural objects. The tool also applies dictionary searches using regular expression searches. The spelling of object descriptions is checked prior to analysis. The NERProject, a Java 8 project included as a sub-tool and part of eBayScraper, provides a way to create a supervised classification using a conditional random field (CRF). The output of this tool is a classification that is used in the NER analysis within eBayScraper. The following provides a high-level overview of the tools provided as well as more detailed instructions on how to use the contents of the tool.

Note:  Until the main branch is updated, users should use the Python 3 branch in this repository. 

<b>Required Libraries</b>

<i>Python</i>

The following libraries are used in eBayScraper and are required (see requirement.txt, used for pip installation, for python libraries), including possibly newer versions of the listed libraries.

Python 2.7+,
nltk==3.4
beautifulsoup4==4.4
ebaysdk==2.1.5 
pysal==2.0
dbfpy==2.0
pyspellchecker==0.5.5
textblob==0.15.2
ctypes==1.0.2
numpy==1.19.1
requests=2.24.0
urllib3==1.25.6
appJar==0.94.0
indexer==0.6.2


<i>Java</i>

The following libraries are used in NERProject and are required, including possibly newer versions of the listed libraries.

Java 8
Stanford CoreNLP 3.9.2:  https://stanfordnlp.github.io/CoreNLP/download.html (see instructions; the lib folder in NERProject has Java libraries needed). You can also need to have the stanford-ner.jar in the lib folder in the main eBayScraper project. This will along with ner-model.ser.gz (or ner model file) will enable the nameEntityReco.py module to function (see /src/nlp in eBayScraper).

<b>High-Level Overview</b>

<b>NER Category Definitions </b>

For category definitions of the NER and dictionary used, see definitions.docx or definitions.pdf.

<i>eBayScraper</i>

1. src/gui
This is a package with the GUI (simpleGUI.py) module. This GUI can be launched using the run.sh script. The GUI allows execution of the scraping, NER/dictionary analysis, removal of duplicate scarped data and output data of the NER/dictionary analysis, and creation of the summary shapefile for sellers. These functions can also be launched as discussed below or conducted via this GUI. The runNER.sh is launched by the option "Build NER Model," which makes the assumption that a .jar called NER_Run.jar executable jar has been created to run the NER model builder. This option should only be used if the jar is created. The runNER.sh may need modification to point to the correct path of the jar, depending where it is placed. Additional modifications to data inputs might be needed, as the NER model creator assums additional data paths (see NERProject below).

2. src/merger

Modules that merge different scraped data (mergeMultipleOutputs.py and mergeMultipleResults.py). The module mergeMultipleOutputs.py merges the outputs of the NER method, while mergeMultipleResults.py merges scraped data. The mergeResults.py integrates the NER/dictionary results with associated countries where items were sold, providing a country-level spatial dataset of the NER/dictionary results. The spatial dataset produced by mergeResults.py provides information on cultures, materials of objects, and general types of objects sold in countries and the dollar value of those sales. 

3. src/nlp

The only module here is nameEntityRecog.py, which applies the named entity recognition technique using the CRF outputs from NERProject. In addition, nameEntityRecog.py conducts dictionary regular expression searches, see inputData folder, as well as spell checks on descriptions. The NER uses the NER model classification (ner-model.ser.gz), which is located in the nlp folder. The output of the analysis is namedEntity.csv placed in the output folder. 

4. src/scraper

The ebayAPI.py is not currently used but it can be applied to directly integrate with the eBay API platform created by eBay. The scrapeData.py is used to scrape data applying the Beautiful Soup library.

5. src/test

The memoryTest.py module is used to test memory availability and allocation in the applied device. The randomSelector.py is used to produce random output from the NER/dictionary results that are applied in memory-recall or other information retrieval tests. 

6. data

The folder that contains the raw scraped data that will be used in the NER model and dictionary analysis done in src/nlp/nameEntityRecog.py. The original raw files are outputted to the output folder but should be moved to this folder for the NER anlaysis or to the totalData folder for merging before NER/dictionary analysis. The data files are .csv files that contain object descriptions, dates of when an eBay item was sold (in the description), the value of the sale, the location of the seller, and the link of the object. The data can be merged together (namedEntityTotal.csv), which will be put in the output folder, or the raw scrape data can be directly incorporated to the data folder without merging and used in NER anlaysis.

7. doc

Folder containing general document descriptions of the modules and functions utilised. More details can be found in the comments within the modules in the src folder.

8. images

Not used currently but could be a location for scraped images from eBay used for analysis.

9. inputData

The folder used for dictionary (i.e., regular express) searches in the NER/dictionary model. See objectExtra.csv

10. output

The output folder used for outputting analysis results in the NER/dictionary model and merger outputs from src/merger. The file namedEntityTotal.csv is the merged scraped data file, while namedEntityMerged.csv is the merged output of the NER/dictionary results. The file nameEntity.csv is the single run output from the NER analysis.

11. shp 

This folder contains a shapefile (TM_WORLD_BORDERS-0.3.shp) used to store data about different countries in the categories analysed for the NER results. The shapefile integrates NER/dictionary analysis data, using src/merger/mergeResults.py, to enable visualization of the results based on country. The data provide a dollar value of antiquities found in different countries as well as type of antiquities/cultural objects, the material in which these objects are made from, and the cultures in which they are associated.

12. totalData

Folder used to place files from scarping and/or NER/dictionary analysis outputs so that they can be merged into one data file. The merging of raw scraped data is done using files here or the outputs from the NER/dictionary analysis as well.

<i>NERProject</i>

1. src/ner

The folder contains two Java objects, which are NERDemo.java and RunTrainer.java respectively. NERDemo.java is an example NER project from the Stanford Natural Language Processing team that is included here as a demonstration on how to use NER. The RunTrainer.java is used for creating the ner-model.ser.gz file, using the Stanford NLP libraries, which is then used in the Python eBayScraper NER analysis (nameEntityRecog.py). The properties.txt is used as a property file applied in RunTrainer.java and is based on requirements from the Stanford tool.

2. bin/ner

The bin folder for Java classes.

3. classifiers

Classifier libraries from the Stanford NLP group.

4. data

Data files used in NERProject/src/ner/RunTrainer.java. The file findEntity.csv is a demo file that demonstrates how terms are parsed and classified using the CRF classifier. The namedEntity.txt file is use for training and creating the CRF model, which, when created, is called ner-model.ser.gz.

5. doc

The Java doc files which provide documentation and explanation of the Java classes utilised in the project folder.

6. lib

The Java libraries (Java 8) used from the Stanford CoreNLP tool.

 <b>Output and Required Input </b>

<i>Key Outputs </i>

To run the NER analysis, scraped data need to be placed in the data folder under eBayScraper. Scraped data are obtained from /src/scraper/scrapedData.py. The make_urls method creates the needed urls to scrape in that module. This will produce output files in the output folder in eBayScraper. These files can be merged together in src/merger/mergeMultipleResults.py, which produced the file namedEntityTotal.csv in the output folder. This process also removes any duplicates of sold data from eBay. The output of the scraping produces an object description, the sale price, the location of the seller, and link of the actual object sold.

The analysis output of the NER is conducted in src/nlp/nameEntityRecog.py, with the output being nameEntity.csv in the output folder. If there are duplicates at this stage, they can be removed by using /src/merger/mergeMultipleOutputs.py. This module could also be used to merge multiple output files if there are multiple outputs. The merged outputs are placed in the output folder under the file namedEntityMerged.csv.

The nameEntity.csv output has the following structure:
Date (date of the sale),Object (description of the object as provided by eBay),Price (the sale price), Location (location where the object was sold),Category (the type of cultural category as determined by the NER/dictionary analysis (e.g., Roman)),Object Type (the type of object (e.g., vessel),Material (the material type of the object (e.g., terracotta),Link (the link to the original object sold).

In the /shp folder in eBayScraper is the file TM_WORLD_BORDERS-0.3.shp. This is a shapefile of the world. The shapefile contains all the category names currently used (e.g., Jewellery, Roman, Viking, Terracotta, etc.) and determines the total dollar value of sales for countries and the top item sold. It also determines how much was sold for given cultural objects (e.g., Roman), material types (e.g., glass), and types of objects (e.g., jewellery). Other terms and categories could be added to the shapefile and analysis if needed by modifying the shapefile and words, objTl, and mat dictionaries in /src/merger/mergeResults.py module. These three dictionaries address cultural (words), object types (objTl), and materials for the objects (mat). The format used for what is currently there in the dictionaries in the module is applied to match cases used in the NER/dictionary analysis and that in the shapefile. 

The file randomSelectionTest.csv is created in the output folder by /src/test/randomSelector.py. The output is the same as namedEntity.csv but only has those lines randomly selected for information retrieval testing. The randomSelector.py module requires a runtime input (e.g., 400 for 400 random selections) in the command line run.  

For the NERProject, the only output is ner-model.ser.gz, which is produced in the data folder under NERProject. This file can be transferred to the /src/nlp folder in eBayScraper to be used for the NER analysis.

<i>Key Inputs</i>

In addition to the scraped data, as discussed above and produced by running /src/sraper/scrapeData.py, users can also add dictionary terms. The long-term goal is not to require the use of a dictionary, as the NER analysis could potentially classify without using a dictionary. However, practically this might not be easy, thus a dictionary is included. The dictionary is in the inputData folder in eBayScraper under the file objectExtra.csv. The following structure is used for the inputs:

Example:  title line:  "jewellery | objectExtra"    
This represents the category term (jewellery) with the "|" indicating the split used to designate if the term is an object description (objectExtra), cultural item (cultures), or a material description (materialType). Each of these three terms have to be used if an object, cultural item, or material description is used.

For terms below the title line, these represent additional terms for a given category term. For example, "america", a cultures designated category, it has the terms "maya", "aztec", "native american", etc. These terms represent "america" based cultures. This is true for all the categories used. The terms below the title line are the terms searched, whereas the title line represents the designation used as the identifier in the outputs of nameEntity.csv. New categories and terms can be created and/or added or removed. All the terms can be included irrespective of capitalization. 

<b>Run Operations and Order</b>

<i> Scraping </i>

1. Run /src/scraper/scrapeData
2. Merge results using /src/merger/mergeMutipleResults.py, which creates nameEntityTotal.csv. Be sure to have the scraped data in the totalData folder. This step could be skipped

<i>NER Model</i>

3. Run /NERProject/src/RunTrainer.java. Can add additional training text to /data/namedEntity.txt

<i>Run NER Analysis and Dictionary</i>

4. Transfer the ner-model.ser.gz file from /NERProject/data/ to eBayScraper/src/nlp/ then run nameEntityRecog.py, with the scraped data files transferred to the data folder or use the nameEntityTotal.csv for the merged scraped data. The output of this will be nameEntity.csv

5. If there are multiple runs, merge the outputs of the NER (taking the results from the output folder) and merge using /src/merger/mergeMutipleOutputs.py, which creates namedEntityuTotal.csv in the output folder. The multiple outputs should be put in totalData. If there is only a single output, this step should be skipped. 

<i>Make into Spatial Data</i>

6. To merge results with location information into the shapefile, run /src/merger/mergeResults.py. Then assess output in the /shp file, which is the same as the shapefile input file (TM_WORLD_BORDERS-0.3.shp). The namedEntityMerged.csv is used as the input. 

<i>Conduct Outputs for Information Retrieval (IR) Tests</i>

7. To select a random number of NER/dictionary results for further testng the utility of the approach (e.g., using precision-recall tests), run /src/test/randomSelector.py on the namedEntityMerged.csv file. 

<i>Flow Diagram</i>

The first six steps from above are represented in the flow diagram attached to this project (RunFlow.jpg). The seventh step is for the IR tests used.

<img src="RunFlow.jpg">
