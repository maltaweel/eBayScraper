package ner;


import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.Scanner;

import edu.stanford.nlp.ie.crf.CRFClassifier;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.sequences.SeqClassifierFlags;
import edu.stanford.nlp.util.StringUtils;

/** 
 * This is the class used for the training of the NER classifier, a type of CRF classifier.
 *  The class uses training data found in namedEntity in the data folder.
 *  The properties of the trainer is found in the ner folder under properties.txt
 *  A test of the classification created is done on the findEntity.csv file
 *  The output classification is ner-moodel.ser.gz found in the data folder
 *
 *  @author Mark Altaweel
 * 
 */
public class RunTrainer {
	
	/**
	 * Main method that launches the trainer to create the classification output found in the data folder.
	 * @param args the runtime arguments given (none used)
	 * @throws Exception any exception that fails to create the classification.
	 */
	public static void main(String[] args) throws Exception {

	   //String modelOutput="../NERProject/output/outputText.txt";
	   String modelOutput="../NERProject/data/ner-model.ser.gz";
	   String prop="../NERProject/src/ner/properties.txt";
	   String trainingFilePath="../NERProject/data/namedEntity.txt";
	   String fileScanner="../NERProject/data/findEntity.csv";
	   
	   RunTrainer rt = new RunTrainer();
	   List<String> output=rt.parseText(fileScanner);
	   rt.trainAndWrite(modelOutput,prop,trainingFilePath);
	   
	   String[] tests = new String[] {"the brutality of Rome and Roman Empire", 
			   "comb hair","band wrist", "barrel clothes", "rome", "earing"};
	   CRFClassifier model=rt.getModel(modelOutput);
	   
	   for (String item : output) {
	     rt.doTagging(model, item);
	   }
			   
	 }
	
	/**
	 * Method to parse the test file findEntity.csv
	 * 
	 * @param file the file findEntity.csv
	 * @return a list of parsed text in relation to the object description 
	 */
	public List<String>parseText(String file){
		
		List<String>output = new ArrayList<String>();
		
		//Get scanner instance
        Scanner scanner=null;
		try {
			scanner = new Scanner(new File(file));
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
         
        //Set the delimiter used in file
        scanner.useDelimiter("\n");
         
        int i=0;
        String s="";
        while (scanner.hasNext())
        {
        	s=scanner.next();
            if (i==0){
            	i++;
            	continue;
            }
            else {
            	output.add(s);
            	i++;
            }
        }
         
        //Do not forget to close the scanner 
        scanner.close();
        
		return output;
	}
	
	/**
	 * Method calls the CRF classifier from the Stanford NLP library.
	 * 
	 * @param modelOutPath the output path for the trained classification
	 * @param prop the properties file used.
	 * @param trainingFilepath the training data file path.
	 */
	public void trainAndWrite(String modelOutPath, String prop, String trainingFilepath) {
		   Properties props = StringUtils.propFileToProperties(prop);
		   props.setProperty("serializeTo", modelOutPath);
		   //if input use that, else use from properties file.
		   if (trainingFilepath != null) {
		       props.setProperty("trainFile", trainingFilepath);
		   }
		   SeqClassifierFlags flags = new SeqClassifierFlags(props);
		   CRFClassifier<CoreLabel> crf = new CRFClassifier<>(flags);
		   crf.train();
		   crf.serializeClassifier(modelOutPath);
		}
	
	/**
	 * Method return the classifier model from the model path
	 * @param modelPath the model path.
	 * @return
	 */
	public CRFClassifier getModel(String modelPath) {
	    return CRFClassifier.getClassifierNoExceptions(modelPath);
	}
	
	/**
	 * Method to tag and classify example text to view the efficacy of the classifier.
	 * @param model the CRF model used.
	 * @param input the input text to test
	 */
	public void doTagging(CRFClassifier model, String input) {
		  input = input.trim();
		  System.out.println(input + "=>"  +  model.classifyToString(input));
		}


}
