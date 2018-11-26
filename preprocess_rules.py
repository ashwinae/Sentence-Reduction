 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 19:27:46 2018

@author: Ashwin
"""

import en_core_web_sm
nlp = en_core_web_sm.load()
import itertools, collections
from collections import Counter
import re

####################################################################################    
def clean_data(string, nlp_model = False, noise = False, no_numbers = False):
    if(type(string) == int or type(string) == float):
        return ""
    string_new = string.lower()
    
    english = {
            "i/m" : "i'm", "'ll": " will", "'ve": " have", "'re":" are","'ve": " have", "can't": "cannot", "won't": "would not", 
            "don't": "do not", "haven't": "have not", "isn't": "is not", "wouldn't": "would not", "couldn't": "could not", 
            "doesn't": "does not", "wont": "would not", "cant": "can not", "dont": "do not", "havent": "have not", 
            "doesnt": "does not", "wouldnt": "would not", "couldnt": "could not", "isnt": "is not", "//": "", "*": "",
              }
    
    for error, replacement in english.items():
        string_new = string_new.replace(error, replacement)
    
    string_new = re.sub("[;]", ".", string_new)
    
    if(no_numbers == True):
        string_new = re.sub("[^a-zA-Z'-.:/,]", " ", string_new)
    else:
        string_new = re.sub("[^a-zA-Z0-9'-/.:,]", " ", string_new)
        
    string_new = string_new.replace("'s", "s")
    split = string_new.split()
    if(len(split) > 0):
        split[len(split) - 1] = re.sub("[^a-zA-Z]", "", split[len(split) - 1])    
    
    if(noise == True):
        string_new = [w for w in split if not w in noise_set]
    
    if(nlp_model == True):
        return nlp(' '.join(split))

    else:
        return ' '.join(split)   
###########################################    
#Function that returns the root words
    #Argument can be a single word, a list of words, or a nested list of words
def get_root(phrases):
    root_words = []
    if(type(phrases) == list):        
        for i in phrases:
            if(type(i) == list):
                doc = nlp(' '.join(i))
                root_words.append([item.lemma_ for item in doc])
            else:
                doc = nlp(i)
                for item in doc:
                    root_words.append(item.lemma_)
                
    else:
        doc = nlp(phrases)
        for item in doc:
            root_words.append(item.lemma_)
        
    return root_words

#get_root([["datas", "nests"], ["glasses"]])
#get_root(["datas", "nests"])
#get_root("nests")

####################################################################################
#Fucntion that returns a nested list of parts of speech present in each statement of a sentence
#In the order of verbs, nouns, adjectives, and adverbs if no argument is given\

def get_pos(data, nouns = False, verbs = False, adjectives = False, adverbs = False, adpositions = False):
    verb_words = list()
    noun_words = list()
    adverb_words = list()
    adjective_words = list()
    adposition_words = list()
    doc = list()
    all_words = list()
    
    if(type(data) == list):
        for i in range(0, len(data)): 
            doc = clean_data(data[i], nlp_model = True)
            
            verb_words.append([str(doc[i]) for i in range(0,len(doc)) if doc[i].pos_ == "VERB"])
            noun_words.append([str(doc[i]) for i in range(0,len(doc)) if doc[i].pos_ == "NOUN"])
            adverb_words.append([str(doc[i]) for i in range(0,len(doc)) if doc[i].pos_ == "ADV"])
            adjective_words.append([str(doc[i]) for i in range(0,len(doc)) if doc[i].pos_ == "ADJ"])
            adposition_words.append([str(doc[i]) for i in range(0,len(doc)) if doc[i].pos_ == "ADP"])
    
            all_words.append(verb_words[i] + noun_words[i] + adjective_words[i] + adverb_words[i] + adposition_words[i])

    else:
        doc = clean_data(data, nlp_model = True)
                
        verb_words = [str(i) for i in doc if i.pos_ == "VERB"]
        noun_words = [str(i) for i in doc if i.pos_ == "NOUN"]
        adverb_words = [str(i) for i in doc if i.pos_ == "ADV"]
        adjective_words = [str(i) for i in doc if i.pos_ == "ADJ"]
        adposition_words = [str(i) for i in doc if i.pos_ == "ADP"]
    
        all_words = verb_words + noun_words + adjective_words + adverb_words
    
    if(nouns == True):
        return noun_words
    if(verbs == True):
        return verb_words
    if(adjectives == True):
        return adjective_words
    if(adverbs == True):
        return adverb_words
    if(adpositions == True):
        return adposition_words
    else:
        return all_words
    
####################################################################################

#Function that returns the words that are present in every single sentence
def important_words(data, nouns = False, adjectives = False, adverbs = False):
 
    noun_words = list()
    adverb_words = list()
    adjective_words = list()

    noun_words = get_pos(data, nouns = True)
    noun_words = get_root(noun_words)
    noun_tuple = [tuple(l) for l in noun_words]
    if(len(noun_tuple > 0)):
        imp_nouns = list(set(noun_tuple[0]).intersection(*set(noun_tuple[1:])))
    else:
        imp_nouns = noun_tuple[0]
    
    adverb_words = get_pos(data, adverbs = True)
    adverb_words = get_root(adverb_words)
    adverbs_tuple = [tuple(l) for l in adverb_words]
    imp_adverbs = list(set(adverbs_tuple[0]).intersection(*set(adverbs_tuple[1:])))
    
    adjective_words = get_pos(data, adjectives = True)
    adjective_words = get_root(adjective_words)
    adjectives_tuple = [tuple(l) for l in adjective_words]
    imp_adjectives = list(set(adjectives_tuple[0]).intersection(*set(adjectives_tuple[1:])))
    
    imp_words = imp_nouns + imp_adverbs + imp_adjectives
        
    if(nouns == True):
        return imp_nouns
    
    elif(adjectives == True):
        return imp_adjectives
    
    elif(adverbs == True):
        return imp_adverbs
    
    else:  
        return imp_words

####################################################################################

#Function that counts the number of times a particular parts of speech word got repeated
def merge_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

def word_counter(data, counter = False):
    #noise_set = ["can", "have", "would", "love", "want", "like", "are", "s"] 
    verbs = list()
    nouns = list()
    adverbs = list()
    adjectives = list()
    adpositions = list()
    
    verbs_counter = Counter(verbs)
    nouns_counter = Counter(nouns)
    adverbs_counter = Counter(adverbs)
    adjectives_counter = Counter(adjectives)
    adposition_counter = Counter(adpositions)
    
    verbs = get_root(get_pos(data, verbs = True))
    if(len(verbs) != 0):
        verbs_counter = collections.Counter(itertools.chain(*verbs))  
    verb_c = { 'verb': sum(verbs_counter.values())}

        
    nouns = get_root(get_pos(data, nouns = True))
    if(len(nouns) != 0):
        nouns_counter = collections.Counter(itertools.chain(*nouns))
    noun_c = { 'noun': sum(nouns_counter.values())}
        
    adverbs = get_root(get_pos(data, adverbs = True))
    if(len(adverbs) != 0):
        adverbs_counter = collections.Counter(itertools.chain(*adverbs))
    adverbs_c = { 'adverb': sum(adverbs_counter.values())}
        
    adjectives = get_root(get_pos(data, adjectives = True))   
    if(len(adjectives) != 0):
        adjectives_counter = collections.Counter(itertools.chain(*adjectives))
    adjectives_c = { 'adjective': sum(adjectives_counter.values())}
    
    adpositions = get_root(get_pos(data, adpositions = True))   
    if(len(adpositions) != 0):
        adpositions_counter = collections.Counter(itertools.chain(*adpositions))
    adpositions_c = { 'adposition': sum(adpositions_counter.values())}    
        
    all_counter = verbs_counter + nouns_counter + adverbs_counter + adjectives_counter + adpositions_counter
    
    pos_counter = merge_dicts(verb_c, noun_c)
    pos_counter = merge_dicts(pos_counter, adverbs_c)
    pos_counter = merge_dicts(pos_counter, adjectives_c)  
    pos_counter = merge_dicts(pos_counter, adpositions_c)
     
    if(counter == True):
        return pos_counter
    
    return all_counter

####################################################################################

#Function to figure out if a verb is transitive or not           
def check_verb(token):
    if token.pos_ == 'VERB':
        indirect_object = False
        direct_object = False
        for item in token.children:
            if(item.dep_ == "iobj" or item.dep_ == "pobj"):
                indirect_object = True
            if (item.dep_ == "dobj" or item.dep_ == "dative"):
                direct_object = True
        if indirect_object and direct_object:
            return 'DITRANVERB'
        elif direct_object and not indirect_object:
            return 'TRANVERB'
        elif not direct_object and not indirect_object:
            return 'INTRANVERB'
        else:
            return 'VERB'
    else:
        return token.pos_
####################################################################################

####################################################################################
#Function to analyze children and head of texts
def head_children(doc):
    for token in doc:
        print(token.text, token.head,
              [child for child in token.children])

#######################################################################################

#Function to get main verbs from an *individual string*
def get_main_verbs(string, main_verb_list = False, data = False):
    
    transitive = []
    main_verb = []
    doc = clean_data(string, nlp_model = True)
    
    for i in range(0,len(doc)):
        if(check_verb(doc[i]) == "TRANVERB"):
            transitive.append(doc[i])
                #Take out words like is, are, have, have been, want and so on        
                        
    if(len(transitive) == 1):
        main_verb.append(transitive[0])
        
    elif(len(transitive) > 1):
        if(data != False):
            yes1 = 0
            yes2 = 0
            for i in range(0, len(data)):
                if(str(transitive[0]) in data[i]):
                    yes1 = yes1 + 1
                if(str(transitive[1]) in data[i]):
                    yes2 = yes2 + 1
                        
            if(yes1 > yes2):
                main_verb.append(transitive[0])
                    
            elif(yes2 > yes1):
                main_verb.append(transitive[1])    
                
#        else:
#            main_verb.append()
            
    elif(len(transitive) == 0):
        for i in range(0, len(doc) - 1):
            if(main_verb_list != False):
                for j in range(0,len(main_verb_list)):
                    if(str(main_verb_list[j]) == str(doc[i])):
                        main_verb.append(main_verb_list[j])
                        break
                    
            if(check_verb(doc[i]) == "INTRANVERB"):
                if(str(doc[i]) == "is"):
                    break
            
                if(check_verb(doc[i+1]) == "ADP"):
                    main_verb.append(doc[i])

                    
                elif(check_verb(doc[i+1]) == "DET"):
                    main_verb.append(doc[i])
                    
                else:
                    main_verb.append(doc[i])
    return main_verb
                        
####################################################################################
#Function to get the main verbs present in a *data set of phrases*
def main_verbs_data(data):
    main_verb = []
    for i in range(0,len(data)):
        for i in get_main_verbs(data[i]):
            main_verb.append(str(i))
                 
    main_verb = list(set(get_root(main_verb)))                 
        
    return main_verb
   
####################################################################################
#Function to obtain the verb-noun phrases from a sentence
def verb_noun_phrase(i, doc, a):
    for j in range(i, len(doc)):
        if(doc[j].pos_ == "NOUN"):
            if(j < len(doc)-2 and doc[j+1].pos_ == "NOUN" and doc[j+2].pos_ == "NOUN"):
                a.append(doc[i:j+3])
            elif(j < len(doc)-1 and doc[j+1].pos_ == "NOUN"):
                a.append(doc[i:j+2])
            else:
                a.append(doc[i:j+1])

###################################################################################

#####################################################################
#Function to remove unwanted words from a sentence or a word_set
def remove_unwanted_words(data, word_set, verb = False, noun = False):
        #not doing part_stem since part_new already satisfies that requirement
    if(noun == True):
        for item in data:
            if(len(item.split()) == 1):
                for doc in nlp(item):
                    if((doc.pos_ == "VERB" or doc.pos_ == "ADP") and str(doc) not in word_set):
                        data.remove(item)
                        break
                        
                        
    if(verb == True):
        for item in data:
            for doc in nlp(item):
                if((doc.pos_ != "VERB") and str(doc) not in word_set):
                    data.remove(item)
                    break
    return data

########################################################################

def remove_super_short(k):
    for phrases in k:
        if(len(phrases) < 2):
            k.remove(phrases)
