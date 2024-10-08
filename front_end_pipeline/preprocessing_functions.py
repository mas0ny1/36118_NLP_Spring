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