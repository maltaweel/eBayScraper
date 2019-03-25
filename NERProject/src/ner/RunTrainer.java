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

public class RunTrainer {
	
	public static void main(String[] args) throws Exception {

	   //String modelOutput="../NERProject/output/outputText.txt";
	   String modelOutput="../NERProject/data/ner-model.ser.gz";
	   String prop="../NERProject/src/ner/properties.txt";
	   String trainingFilePath="../NERProject/data/namedEntity.txt";
	   String fileScanner="../NERProject/data/cantFindEntity.csv";
	   
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
	
	public CRFClassifier getModel(String modelPath) {
	    return CRFClassifier.getClassifierNoExceptions(modelPath);
	}
	
	public void doTagging(CRFClassifier model, String input) {
		  input = input.trim();
		  System.out.println(input + "=>"  +  model.classifyToString(input));
		}


}
