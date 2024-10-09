# preprocessing pipeline for single screenplay texts (one at a time)

# assuming a .txt file has been uploaded to the streamlit interface 
# import functions
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords 
stops = stopwords.words('english') 

# remove unreadable non-ASCII chars 
from preprocessing_funcs import remove_non_ASCII
cleantext = remove_non_ASCII(text)

# TODO: use a BERT to annotate text and format as a dict {label:data} 

# TODO: encode labels if not already encoded

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

# iterate through the dict, assuming that each key is an annotation label, and each value is a preprocessed string
for key, value in text_uncut.items():
    # tokenize that string into a list of sentences 
    text_uncut[key] = sent_tokenize(value)
    # clean up sentences 
    ## removing 'EXT' and 'INT' sentences
    text_uncut[key] = remove_location(value)
    ## remove empty sentences 
    text_uncut[key] = remove_empties(value)
    ## word tokenize sentences
    text_uncut[key] = [word_tokenize(sent) for sent in value]
    ## remove tokens that contain no letter, contain only one char, or are in stopwords
    text_uncut[key] = [
        [token for token in sent 
         if contains_letters(token) 
         and len(token) > 1 
         and token not in stops]
        for sent in value 
    ]

    ## NB: end of pipeline represented in BERT_annotations_preprocessing.ipynb

    ## start of pipeline representented in BERT_lemmatization_json.ipynb

    # join dict data back into a text corpus for spacy wrapping
    text = join_json(text_uncut)

    
  
## TODO:
### convert chars to lower







