# Language Similarity
This project accepts labeled documents containing text from different languages, and calculates cosine similarity, using trigram frequencies, to measure similarty between a known language and an unknown document.

## Input.txt
A file containing languages and associated filenames. A file may be labeled as 'Unknown', and will be compared to all other known languages from the input.

Ex. input:
  > English english1.txt  
  > French french2.txt  
  > English english2.txt  
  > Spanish spanish1.txt  
  > Unknown unknown_text.txt  

## Output.txt
A file containing the calculated similarity between each 'Unknown' document and every 'known' language.

Ex. output:
  > unknown_text.txt:   
  > &nbsp;&nbsp;&nbsp;&nbsp; French:   0.77537    
  > &nbsp;&nbsp;&nbsp;&nbsp; Spanish:  0.6124    
  > &nbsp;&nbsp;&nbsp;&nbsp; English:  0.23128    


# To run:

To run this code, first you must make sure you have created an input file that correctly references existing text documents

Next, run:
    ```python LanguageSimilarity.py <input_name> <output_name> ```
where input_name is the name of the input text file, and output_name is the desired name of the output file.

Check the output file to see your results!
