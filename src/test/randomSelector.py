'''
Module used for testing the results' quality by randomly selecting inputs that are then selected.
External to this, the researcher should apply a precision-recall or other information retrieval test.

Created on Mar 25, 2019

@author: 
'''
import os
import random
import csv
import sys

'''
Method to generate random numbers and provide test data to assess for evaluation in information retrieval methods.
The selection of data is based on the length of the input (the output file from NER called namedEntity.csv in output) 
and number of random selections to make.

@param n- the number of random selections to make
@return returns- the randomly selected data to print.
'''
def selectRandom(n):
    
    print "run random"
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'output','namedEntityMerged.csv')

    returns=[]
    
    #this looks at the data and then returns the desired number of random samples
    row_count=0
    with open(os.path.join(pathway),'rU') as csvfile:
        row_count = sum(1 for row in csvfile)
    
    with open(os.path.join(pathway),'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        rows=[r for r in reader]
    
        numbers=[]
        for i in range(1,n):
  #          print(random.randint(10000,100000))
            numbers.append(random.randint(1,row_count))
    
        
        for x in numbers:
            returns.append(rows[x-1])
                
        
    return returns

'''
Method to print the results of the random selection of output data.
@param the results to print from the random selection in a file called randomSelectionTest found in the output folder
'''
def printResults(results):
    
    fieldnames = ['Date','Object','Price','Location','Category','Object Type','Material','Link']
     
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    fileOutput=os.path.join(pn,'output',"randomSelectionTest.csv")
    
    #write output file including data from results of the NER/dictionary analysis
    with open(fileOutput, 'wb') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()    
        for d in results:
           
            
            res0=d['Date']
            
            res1=d['Object']
            res2=d['Price']
            res3=d['Location']
            res4=d['Category']
            res5=d['Object Type']
            res6=d['Material']
            res7=d['Link']
            
            writer.writerow({'Date': str(res0),'Object':str(res1),'Price':str(res2),'Location':str(res3),
                             "Category":str(res4),'Object Type':str(res5),'Material':
                             str(res6),'Link':str(res7)})  
    
'''
Method to run the module. An runtime input is required to provide the random
number of selections to chose. This number is given in the command line arguments 
(e.g., 400 for 400 random selections).
'''    
def run():
    #take an input argument (i.e., the number of random selections from results)
    n = int(sys.argv[1])
    
    #select random data
    results=selectRandom(n)
    
    #print those results of the random selection of analysed data
    printResults(results)
   
if __name__ == '__main__':
    run()

