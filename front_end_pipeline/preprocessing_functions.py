# preprocessing functions 
import re

# remove non_ascii chars
def remove_non_ascii(text):
    hex_pat = re.compiled(r'[\x00-\x1F\x7F-\x9F]')
    cleantext = re.sub(hex_pat, '', text)
    return cleantext


# flatten data assigned to each annotation
def flatten_data(dict_list, key):
    flattened_data = []
    temp = ''
    for d in dict_list:
        if key in d:
            temp += ' ' + d[key] if temp else d[key]
        else:
            # if a key other than input is encountered and temp is not empty
            if temp:
                # append the concatenated string to text list 
                flattened_data.append({key:temp})
                # and reset temp 
                temp = ''
            # append non text dict to list 
            flattened_data.append(d)
    # after loop ends, concatenate what's left in temp if anything
    if temp:
        flattened_data.append({key:temp})
    # and return concatenated list
    return flattened_data

# remove speaker_heading data 
def decapitate_speakers(dict_list):
    decapitated = [d for d in dict_list if not 'speaker_heading' in d]
    return decapitated 

# remove empty strings and punctuations
def remove_nulls(dict_list):
    import string
    puncts = set(string.punctuation)
    non_nulls = []
    for dict in dict_list:
        valid = True
        for val in dict.values():
            if val == '' or all(char in puncts for char in val):
                valid = False
                break
        if valid:
            non_nulls.append(dict)
    return non_nulls

# delete strings containing 'CUT' 
def delete_cuts(dict_list):
    import re 
    # empty list for filtered dicts
    dicts_uncut = []
    for d in dict_list:
        # if none of the values in the dict match 'CUT'
        if all(not re.search(r'CUT', str(val)) for val in d.values()):
            # then append to list
            dicts_uncut.append(d)
    return dicts_uncut 

# function to remove irrelevant location info 'EXT|INT'
def remove_location(sentences):
    return [sent for sent in sentences if sent not in ['EXT.', 'INT.', 'ext.', 'int.']]

# function to remove empty sentences 
def remove_empties(sentences):
    return [sent for sent in sentences if sent]

# check if a token contains letters
def contains_letters(token):
    return bool(re.search(r'[a-zA-Z]', token))

# function for rejoining dict data back into text
def join_json(data):
    # empty list for storing joined lines (one line per dict)
    joined_lines = []
    # iterate through dicts
    for d in data:
        # unpack keys and values
        for key, value in d.items():
            # convert key to string label with an escape char
            label = '@' + str(key) + ':'
            # append label to corpus
            joined_lines.append(label)
            # create an empty list for joined sentences 
            joined_sentences = []
            # iterate through sentences in value
            for sentence in value:
                # join the sentences with " " 
                joined_sentence = " ".join(sentence)
                # append joined_sentence to joined_sentences
                joined_sentences.append(joined_sentence)
            # now join the sentences in joined_sentences with ". "
            sentences_in_line = ". ".join(joined_sentences)
            # append this line to the joined_lines list
            joined_lines.append(sentences_in_line)
    # now join all the lines in joined_lines with "\n"
    screenplay_text = " \n ".join(joined_lines)
    # and return the text
    return screenplay_text
