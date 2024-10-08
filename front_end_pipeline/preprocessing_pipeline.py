# preprocessing pipeline for single screenplay texts (one at a time)

# assuming a .txt file has been uploaded to the streamlit interface 
# import functions
# remove unreadable non-ASCII chars 
from preprocessing_funcs import remove_non_ASCII
cleantext = remove_non_ASCII(text)

# use a BERT to annotate text and format as a dict {label:data} 

# flatten text data 
flat_text = flatten_data(text_annot, 'text')

# flatten dialog data 
flattened_text = flatten_data(flat_text, 'dialog')

# remove speaker_heading data 
decapitated_text = decapitate_speakers(flattened_text)

# remove empty strings
text_nonna = remove_nulls(decapitated_text)

# delete 'CUT' strings
text_uncut = delete_cuts(text_nonna)

# sentence tokenize each value 
import nltk
from nltk.tokenize import sent_tokenize 
nltk.download('punkt_tab')

# empty list for storing results 
sents = [] 

for dict in texts_uncut:
    # empty dict for storing results
    sents_dict = {}
    for key, value in dict.items():
        sents_dict[key] = sent_tokenize(value)
        sents.append(sents_dict)
