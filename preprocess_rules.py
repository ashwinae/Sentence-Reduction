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
import requests
from common import appglobals



####################################################################################    
def clean_data(string, nlp_model = False, noise = False, no_numbers = False):
    if(type(string) == int or type(string) == float):
        return ""
    string_new = string.lower()
    string_new = " " + string_new + " "
    hindi = {
          " nhi ":" nahi ", " ni ": " nahi ", " rha ": " raha ", " rhi ": " rahi ", " rhe ": " rahe ",
          " kala ": " kaala ", " bhe " : " bhi ", " bde ": " bade ", " gya ": " gaya ", " gyi ": " gayi ",
          " gye ": " gaye ", " h ": " hai ", " hi ": " hai ", " pechle ": " pichle ", " neche ": " neeche ",
          " uth " : " uht ", " utha ": " uhta ", " uthane ": " uhtane ", " uthi ": " uhti ", " toot ": " tut ",
          " thooth ": " tut ", " khrab ": " kharaab ", " jayada ": " zyada ", " jada ": " zyada ", " mai ": " mein ",
          " jyada ": " zyada ", " jaidha ": " zyada ", " dam ": " dum ", " pr ": " par ", " karna ": " krna ",
          " gai ": " gayi ", " gya ": " gaya ", " nahe ": " nahi ", " mai ": " mein ", " me ": " mein ",
          " main ": " mein ", " khrabi ": " kharaabi ", " k ": " ke ", " Kam ": " kaam ", " pise ": " paise ",
          " chllta ": " chaltha ", " chlte " : " chalthe ", " garm ": " garam ", " upor ": " upar ", " km ": " kaam ",
          " korta ": " kartha ", " pehali ": " pehli ", " phle ": " pehle ", " chta ": " chaahta ", " tel ": " thel ",
          " krana ": " karaana ", " krani ": " karaani ", " krwana " : " karwaana ", " kharap ": " kharaab ",
          " avaj ": " awaaz ", " kikaam ": " ki kaam ", " lga ": " laga ", " lgaa " : " laga ", " traf ": " taraph ", 
          " geer ": " ghir ", " lagte ": " lagate ", " apneap ": " apne aap ", " lia ": " liya ",
          " koi ": " koyi ", " bar ": " baar ", " age ": " aage ", " hae ": " hai ", " aarahi ": " ah rahi ", " ghees ": " ghis ",
          " h.": " hai."
          }
    
    english = {
            " lood ": " load ", " lod ": " load ", " roop ": " rope ", " staarter ": " starter ", " new trul ": " neutral ",
            " filtor ": " filtor ", " jaam ": " jam ", " slipe ": " slip ", " engin ": " engine ", " overhit ": " overheat ",
            " macanic ": " mechanic ", " selry ": " salary ", " gyre ": " gear ", " gayer ": " gear ", " heaigh ": " high ",
            " seel ": " seal ", " hitting ": " heating ", " rediyetor ": " radiator ", " capecty ": " capacity ", " likig " : " leakage ",
            " hourse ": " hour ", " tide " : " tight ", " overheting ": " overheating ", " digal ": " diesel ", " desiele " : " diesel ",
            " plait ": " plate ", " palet ": " plate ", " ptale ": " plate ", " betery ": " battery ", " stape ": " step ", " lik ": " leak ",
            " tyre ": " tire ", " tayer ": " tire ", " frant ": " front ", " nd ": " and ", " pitsion ": " piston ", 
            " troli ": " trolley ", " metor ": " meter ", " lek ": " leak ", " lak ": " leak ", " waring ": " wiring ", 
            " viring ": " wiring ", " dawn ": " down ", " damig ": " damage ", " out-put ": " output ", " eigine ": " engine ",
            " stering " : " steering ", " stairing ": " steering ", " hydrolic ": " hydraulic ", " hich ": " hitch ", " creack " : " crack ",
            " crcke ": " crack ", " cluth ": " clutch ", " servise ": " service ", " sarivis ": " service ", " searvice " : " service ",
            " automatuicly " : " automatically ", " problam ": " problem ", "i/m" : "i'm", "'ll": " will", "'ve": " have", "'re":" are",
            "'ve": " have", "can't": "cannot", "won't": "would not", "don't": "do not", "haven't": "have not", "isn't": "is not", 
            "wouldn't": "would not", "couldn't": "could not", "doesn't": "does not", "wont": "would not", "cant": "can not", "dont": "do not",
            "havent":   "have not", "doesnt": "does not", "wouldnt": "would not", "couldnt": "could not", "isnt": "is not", "//": "", "*": "",
            " colling ": " cooling ", " awaj ": " awaaz ", " aawaj ": " awaaz ", " chk ": " check ", " chak ": " check ", " chake ": " check ",
            " instt ": " instruction ",   " likeg ": " leakage ", " fual ": " fuel ", " chanse ": " change ", " hei ": " he "
             }
    
#    spell_checked = ""
#    d = enchant.Dict("en_US")

#    for item in string_new.split():
#        spell_checked += spell(item) + " "
#    spell("warking")
    
    for error, replacement in hindi.items():
        string_new = string_new.replace(error, replacement)
        
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

####################################################################################   
     
def get_phrases(data):
    a = list()
    noun_phrases = 0
    data_verbs = main_verbs_data(data)

    for i in range(0,len(data)):
        neg = ""
        question = 0
        b = list()
        doc = clean_data(data[i], nlp_model = True)
    
        for i in range(0, len(doc)):
            if(doc[i].dep_ == "neg"):
                neg = doc[i]
               
        if(len(neg) != 0):
            continue
      
        transitive = []
        
        for i in range(0,len(doc)):
            if(check_verb(doc[i]) == "TRANVERB"):
                transitive.append(doc[i])        
                
        for i in range(0,len(doc)):    
            if(len(transitive) == 0):
                if(((doc[i]).tag_ == "WP") or (doc[i].tag_ == "WRB")):
                    words = important_words(data)
                    lemma = []
                    for each in doc:
                        lemma.append(each.lemma_)
                        question = 1
                
        if(question == 1):  
            for i in range(0, len(doc)):
                if(set(words).issubset(set(lemma))):
                    if((doc[i].pos_ == "NOUN") and (i != len(doc)-1)):
                        if(doc[i].tag_ != "WP" and doc[i].tag_ != "WRB"):
                            verb_noun_phrase(i , doc, a)                                    
                            noun_phrases = 1
                continue
    
        #Adverbs can be aptly handled
                
        if(len(transitive) == 1):
            for i in range(0, len(doc)):
                if(str(doc[i]) == str(transitive[0])):
                    verb_noun_phrase(i, doc, a)
                    verb_noun_phrase(i, doc, b)
                            
        elif(len(transitive) > 1):
            yes1 = 0
            yes2 = 0
            for i in range(0, len(data)):
                if(str(transitive[0]) in data[i]):
                    yes1 = yes1 + 1
                if(str(transitive[1]) in data[i]):
                    yes2 = yes2 + 1
                    
                if(yes1 > yes2):
                    for i in range(0, len(doc)):
                        if(str(doc[i]) == str(transitive[0])):
                            verb_noun_phrase(i, doc, a)
                            verb_noun_phrase(i, doc, b)
                            
                elif(yes2 > yes1):
                    for i in range(0, len(doc)):
                        if(str(doc[i]) == str(transitive[1])):
                            verb_noun_phrase(i , doc, a)
                            verb_noun_phrase(i , doc, b)
                #if(len(b) == 0):

        elif(len(transitive) == 0):
            for i in range(0, len(doc) - 1):
                for j in range(0,len(data_verbs)):
                    if(str(data_verbs[j]) == str(doc[i])):
                        verb_noun_phrase(i , doc, a)
                        verb_noun_phrase(i , doc, b)
                        continue
                                    
                if(check_verb(doc[i]) == "INTRANVERB"):
                    if(str(doc[i]) == "is"):
                        continue
                
                    if(check_verb(doc[i+1]) == "ADP"):
                        verb_noun_phrase(i , doc, a)
                        verb_noun_phrase(i , doc, b)
                    
                    elif(check_verb(doc[i+1]) == "DET"):
                        verb_noun_phrase(i , doc, a)
                        verb_noun_phrase(i , doc, b)
                        
                    else:
                        verb_noun_phrase(i , doc, a)
                        verb_noun_phrase(i , doc, b)
        
        if(len(b) == 0):
            noun_phrases = 1
   
    if(noun_phrases == 1):
        for i in range(0,len(data)):
            doc = clean_data(data[i], nlp_model = True)
            for i in range(0, len(doc)):
                if(doc[i].pos_ == "NOUN" and i != len(doc)-1):  
                    verb_noun_phrase(i , doc, a)
                    
    remove_super_short(a)
        
    imp_words = important_words(data)
    
    if(len(imp_words) != 0):
        
        phrases = list()
    
        #Conditions to make sure that the phrases belong to the same intent 
        for i in range(0,len(a)):
            lemma = []
            for each in a[i]:
                lemma.append(each.lemma_)
                
            if(set(imp_words).issubset(set(lemma))):
                phrases.append(a[i])
        phrases = list(set([str(phrases[i]) for i in range(0, len(phrases))]))  
        return phrases
    
    a = list(set([str(a[i]) for i in range(0, len(a))]))      
    return a

###########################################################################

####################################################################################
#To eliminate similar expressions (suited to dialogflow)  
def remove_similar(examples): 
    main_verbs = main_verbs_data(examples)
    
    examples1 = []
    for items in examples:
        examples1.append(clean_data(items, nlp_model = True)) 
    
    tags = ["ADJ", "VERB", "NUM", "ADV", "NOUN", "ADP"]
    new_phrases=[]
    for item in examples1:
        new_phrases.append(item)

    for doc1 in examples1:
        for doc2 in examples1:
            
            if((doc1 in new_phrases) and (doc2 in new_phrases) and (doc1 != doc2)):

                verb1 = get_main_verbs(str(doc1), main_verbs, examples)
                verb2 = get_main_verbs(str(doc2), main_verbs, examples)
                
                if(len(verb1) == 0 or len(verb2) == 0):
                    continue
                verb1 = verb1[0]
                verb2 = verb2[0]
                verb1 = [doc.lemma_ for doc in nlp(str(verb1))]
                verb2 = [doc.lemma_ for doc in nlp(str(verb2))] 
                        
                remaining1_tags = list()
                remaining2_tags = list()
                
                lemma1 = list()
                for each in doc1:
                    lemma1.append(each.lemma_)

                lemma2 = list()
                for each in doc2:
                    lemma2.append(each.lemma_)

                intersection = [value for value in lemma1 if value in lemma2]   
                remaining1 = [w for w in lemma1 if not w in intersection]
                remaining2 = [w for w in lemma2 if not w in intersection]
                                    
                for each in nlp(' '.join(lemma1)):
                    for token in remaining1:
                        if(token == str(each)):
                            if(each.pos_ in tags):
                                remaining1_tags.append(each.pos_)
                                                    
                for each in nlp(' '.join(lemma2)):
                    for token in remaining2:
                        if(token == str(each)):
                            if(each.pos_ in tags):
                                remaining2_tags.append(each.pos_)
                                    
                if(verb1 == verb2):
                            
                    if(len(doc1) == len(doc2)):
                                
                        if(len(intersection) == len(doc1)):
                            new_phrases.remove(doc1)
                            
                        #if(len(intersection) != len(doc1)):
                        if(abs(len(doc1) - len(doc2) == 1)):
                                    
                            if(len(remaining1) < 2):
                                if(len(remaining1_tags) == 0):
                                    new_phrases.remove(doc1)
                                    
                            if(len(remaining2) < 2):
                                if(len(remaining2_tags) == 0):
                                    new_phrases.remove(doc2)
                            
                            if(remaining1_tags == remaining2_tags):               
                                
                                if(len(remaining1) == 1 and len(remaining2) == 1):
                            
                                    all_counter = word_counter(new_phrases)
                                    if(all_counter[remaining1[0]] > all_counter[remaining2[0]]):
                                        new_phrases.remove(doc1)
                                    elif(all_counter[remaining1[0]] < all_counter[remaining2[0]]):
                                        new_phrases.remove(doc2)
                                                   
                    elif(len(doc1) != len(doc2)):
                        if(len(intersection) == len(doc1)):
                            if(len(doc2) - len(intersection) < 2):
                                if(len(remaining2_tags) == 0):
                                    new_phrases.remove(doc2)
                
                if(verb1 != verb2):
                    if(len(doc1)== len(doc2)):
                        if(len(intersection) == len(doc1) - 1):
                            all_counter = word_counter(new_phrases)
                            if(all_counter[remaining1[0]] > all_counter[remaining2[0]]):
                                new_phrases.remove(doc1)
                            elif(all_counter[remaining1[0]] < all_counter[remaining2[0]]):
                                new_phrases.remove(doc2)

    new_phrases = list(set([str(new_phrases[i]) for i in range(0, len(new_phrases))]))                         
    return new_phrases   
####################################################################################
    
def sentence_reduction(doc, data = None, single_phrase = False):
    
    noise_set = ["is", "are", "were"]
    a = list()
    noun_phrases = 0
    main_verb = list()
    neg = ""
#   question = 0
    doc = clean_data(doc, nlp_model = True)
    
    for i in range(0, len(doc)):
        if(doc[i].dep_ == "neg"):
            neg = doc[i]
               
    if(len(neg) != 0):
        return str(doc)
      
    transitive = []
        
    for i in range(0,len(doc)):
        if(check_verb(doc[i]) == "TRANVERB"):
            transitive.append(doc[i])        
                   
    if(len(transitive) == 1):
        main_verb.append(transitive[0])
        for i in range(0, len(doc)):
            if(str(doc[i]) == str(transitive[0])):
                verb_noun_phrase(i, doc, a)
                            
    elif(len(transitive) > 1 and data != None):

        for i in range(0, len(data)):
            for i in range(0, len(doc)):
                if(str(doc[i]) == str(transitive[0])):
                    verb_noun_phrase(i, doc, a)
                            
                if(str(doc[i]) == str(transitive[1])):
                        verb_noun_phrase(i , doc, a)

    elif(len(transitive) == 0):
        for i in range(0, len(doc)):
            if(check_verb(doc[i]) == "INTRANVERB" and str(doc[i]) not in noise_set):
                if(i < len(doc) - 1):
                
                    if(check_verb(doc[i+1]) == "ADP"):
                        main_verb.append(doc[i])
                        verb_noun_phrase(i , doc, a)
                    
                    elif(check_verb(doc[i+1]) == "DET"):
                        main_verb.append(doc[i])
                        verb_noun_phrase(i , doc, a)
                        
                    else: 
                        main_verb.append(doc[i])
                        verb_noun_phrase(i , doc, a)
                else:
                    main_verb.append(doc[i])
                    for j in range(0, len(doc)):
                        if(doc[j].pos_ == "NOUN"):
                            a.append(doc[j:len(doc)])
        
    if(len(a) == 0):
        noun_phrases = 1
   
    if(noun_phrases == 1 and data != None):
        for i in range(0,len(data)):
            doc = clean_data(data[i], nlp_model = True)
            for i in range(0, len(doc)):
                if(doc[i].pos_ == "NOUN" and i != len(doc)-1):  
                    verb_noun_phrase(i , doc, a)
                    
#    remove_super_short(a)

    a = list(set([str(a[i]) for i in range(0, len(a))])) 
    
    if(len(a) == 0):
        return ""
    
    if(single_phrase == True):
        duplicate = []
        for item in a:
            duplicate.append(item)
        counter_list = []

        if(len(a) > 0):
            for i in range(1, len(a)):
                if(a[i-1] in duplicate and a[i] in duplicate):
                    if(len(a[i-1]) > len(a[i])):
                        temp = a[i-1].rsplit(a[i])
                        counter_list = word_counter(temp, counter = True)
                        if(counter_list['adposition'] > 0 and counter_list['noun'] > 0):
                            if(('because' or 'due') in word_counter(temp).keys()):
                                duplicate.remove(a[i])
                                break

                        if(counter_list['adverb'] > 0 and counter_list['noun'] > 0):
                            duplicate.remove(a[i-1])
                            break
                        if(counter_list['noun'] > 0):
                            duplicate.remove(a[i])
                            break
                    else:
                        temp = a[i].rsplit(a[i-1])
                        counter_list = word_counter(temp, counter = True)
                        if(counter_list['adposition'] > 0 and counter_list['noun'] > 0):
                            if(('because' or 'due') in word_counter(temp).keys()):
                                duplicate.remove(a[i])
                                break
                        if(counter_list['adverb'] > 0 and counter_list['noun'] > 0):
                            duplicate.remove(a[i])   
                            break
                        if(counter_list['noun'] > 0):
                            duplicate.remove(a[i-1])   
                            break
                        
            if(len(duplicate) > 0):
                phrases_new = []
                min_count = 255
                min_thing = ""
                for item in duplicate:
                    if(len(item.split()) < min_count):
                            min_count = len(item.split())
                            min_thing = item
                phrases_new.append(min_thing)
            
                return phrases_new[0]
        
        return duplicate
        
    return a
################################################################################

################################################################    

def convert_punctuation_to_dots(input_string):
    noise = ['unit', 'anything', 'item', 'customer']
    punctuation = ['-', ',']
    doc = clean_data(input_string, nlp_model = True, no_numbers = False)
    if(len(doc) == 0):
        return input_string
    problems = ["leak", "leakage", "leaking", "leaks", "fill", "moisture", "light", "short", "fuse", "sparks", "spark", 
                 "power", "current", "voltage", "circuit", "dead", "on", "light",
                 "latch", "dent", "crack", "snap", "damage", 
                 "dry", "dried", "drying",
                 "close", "shut", "shuts", "high", "low", "height",
                 "spin", "seal", "drain",
                 "lock", "noise", "sound", "loud", "noisy",
                 "freeze", "icing", "frozen", "work", "start", "run", "come", "cool",
                 "cold", "ring", "rust", "heat", "hot", "warm",
                 "fit", "fitting", "jamming", "jammed", "jam", "stuck"]
    nouns = ["ice", "maker", "door", "handle", "plug", "part"]
    already_present = []
    
    for item in doc:
        new = [str(item) for item in doc]
    
    #Dashes and commas that precede a verb are converted into dots. Everything else is retained the same way they are.
    for i in range(1, len(doc)):
        
        if(str(doc[i]) in punctuation):
            
            if(doc[i-1].pos_ == "VERB" or "NOUN" or "ADJ" or "issues" or "issue"): #and doc[i+1].pos_ != "VERB"):
                new[i] = '.'

    #Checks if '.' is ineeded necessary
    phrases = (' '.join(new).split('.'))
    phrases = list(filter(None, phrases))
    phrases = [item.strip() for item in phrases]
            
    if(len(phrases) > 1):
        for j in range(0,len(phrases)):    
            split_words = phrases[j].split()
            
            for i in range(1, len(split_words)):
                if(i < len(split_words)):
                    if(split_words[i-1] == split_words[i]):
                        split_words.pop(i)
        
            phrases[j] = ' '.join(split_words)
        
        temp_phrases = []
        for i in phrases:
            temp_phrases.append(i)
        
        for j in range(0, len(phrases)):
            count = 0
            if(j > len(phrases) - 1):
                break
            
            individual_words = phrases[j].split()
        
            if(("issues" or "issue") in individual_words and j == 0):
                continue
        
            if(("issues" or "issue") in individual_words and j != 0):
                phrases[j] = '. ' + phrases[j]
                continue        
    
            phrases[j] = ' '.join(individual_words)

            if("and" in phrases[j]):       
                individual_phrases = phrases[j].split("and")
                individual_phrases = list(filter(None, individual_phrases))
                individual_phrases = [item.strip() for item in individual_phrases]
            
                for i in range(0, len(individual_phrases)):
                    noun_words = get_pos(individual_phrases[i], nouns = True)
                    verb_words = get_pos(individual_phrases[i], verbs = True)
            
                    if((len(individual_phrases[i].split()) == 1 and len(verb_words) == 1) or (len(verb_words) == 0 and len(noun_words) > 0)):
                        if(i == 0):
                            individual_phrases[i] = individual_phrases[i] + ' and '
                            continue
                
                        elif(len(get_main_verbs(individual_phrases[i-1])) != 0):
                            individual_phrases[i] = ' and ' + individual_phrases[i] 
                            
                        elif(i < len(individual_phrases) - 2 and len(get_main_verbs(individual_phrases[i+1])) != 0):
                            individual_phrases[i] = individual_phrases[i] + " and"
        
                    else:
                        if(i != 0):
                            word = individual_phrases[i-1].split()
                            if(len(word)!=0):
                                if(word[len(word)-1] != "and"):
                                    individual_phrases[i] = '. ' + individual_phrases[i]
                
                phrases[j] = ' '.join(individual_phrases)
                
                if(j != 0):
                    phrases[j] = ". " + phrases[j]
                continue
            
            noun_words = get_pos(phrases[j], nouns = True)
            verb_words = get_pos(phrases[j], verbs = True)
        
            if(len(noun_words) != 0):
                for i in noise:
                    if(i in noun_words):
                        noun_words.remove(i)
        
            for word in individual_words:
                if(word in problems and word not in already_present and j!= 0):
                    phrases[j] = '. ' + phrases[j]
                    already_present.append(word)
                    count = 1
        
            if(count == 1):
                continue
        
            if(len(get_main_verbs(phrases[j])) != 0 and j != 0):      ##MAKES USE OF MAIN VERBS FUNCTION   
                phrases[j] = '. ' + phrases[j]
                continue

            if(len(get_main_verbs(phrases[j])) == 0 and j != 0):    
                if(len(phrases[j].split()) == 1 and len(noun_words) == 1):
                    if(("issues" or "issue") in phrases[j-1].split()):
                        temp_phrases.remove(phrases[j])
                        continue
                    else:
                        phrases[j] = "and " + phrases[j]
                        count = 1       
                        continue                        
            
                elif(len(noun_words) == 1):                       
                    if(len(verb_words) == 0):
                        temp_phrases.remove(phrases[j])
                        count = 1  
                        continue
                
                elif(len(noun_words) == 0):
                    temp_phrases.remove(phrases[j])
                    continue

                elif(len(noun_words) > 1):
                    temp_count = 0
                    for i in noun_words:
                        if(i in nouns):
                            temp_count = 1
                    if(temp_count == 0):
                        temp_phrases.remove(phrases[j])
                        continue
                
                else:
                    phrases[j] = '. ' + phrases[j]
                
        
            if(len(get_main_verbs(phrases[j])) == 0 and j == 0):    
                if(len(noun_words) == 1 and len(verb_words) == 0):
                    temp_phrases.remove(phrases[j])
                    continue
             
            phrases[j] in temp_phrases
#            elif(len(noun_words) == 0):
                
#               phrases.remove(phrases[j])
#               count = 1 
                
            if(count == 0 and j != 0):
                phrases[j] = '. ' + phrases[j]
                continue
        
            phrases = list(filter(None, phrases))
          
    if(len(phrases) == 1):
        
        phrases = phrases[0].split("and")
        phrases = list(filter(None, phrases))
        phrases = [item.strip() for item in phrases]
        
        temp_phrases = []
        for item in phrases:
            temp_phrases.append(item)
            
        for i in range(0, len(phrases)):
            noun_words = get_pos(phrases[i], nouns = True)
            verb_words = get_pos(phrases[i], verbs = True)
            
            if((len(phrases[i].split()) == 1 and len(verb_words) == 1) or (len(verb_words) == 0 and len(noun_words) > 0)):
                if(i == 0):
                    phrases[i] = phrases[i] + ' and '
                    continue
                
                elif(len(get_main_verbs(phrases[i-1])) != 0):
                    phrases[i] = 'and ' + phrases[i] 
                    
                elif(i < len(phrases) - 2 and len(get_main_verbs(phrases[i+1])) != 0):
                    phrases[i] = phrases[i] + " and"
        
            else:
                if(i != 0 and phrases[i-1].split()[len(phrases[i-1].split())-1] != "and"):
                    phrases[i] = '. ' + phrases[i]
    
    check_phrases = []
    for i in phrases:
        check_phrases.append(i)
     
    for i in range(0,len(temp_phrases)):
        temp_phrases[i] = re.sub("[^a-zA-Z0-9/]", " ", temp_phrases[i]) 
        temp_phrases[i] = re.sub("and ", "", temp_phrases[i])
        temp_phrases[i] = temp_phrases[i].strip()
        temp_phrases[i] = re.sub(' +', ' ',temp_phrases[i])
        
        
    item = check_phrases[0]
    for item in check_phrases:
        item_clean = re.sub("[^a-zA-Z0-9/]", " ", item)
        item_clean = re.sub("and ", "", item_clean)
        item_clean = item_clean.strip()
        item_clean = re.sub(' +', ' ',item_clean)
        if(item_clean not in temp_phrases):
            check_phrases.remove(item)
    
    phrases = check_phrases

    for i in range(0, len(phrases)):
        individual_words = phrases[i].split()
        for word in nlp(phrases[i]):
            if(word.pos_ == "ADV" and word.text != "not"):
                if(str(word) in individual_words):
                    individual_words.remove(str(word))
    
        for k in range(1, len(individual_words)):
                if(k < len(individual_words)):
                    if(individual_words[k-1] == individual_words[k]):
                        individual_words.pop(k)
    
        if(i == 0 and len(individual_words) > 0 and individual_words[0] == '.'):
            individual_words.pop(0)
            
        if(len(individual_words) > 0 and individual_words[len(individual_words)-1] == "and"):
            individual_words.pop(len(individual_words) - 1)
        
        phrases[i] = ' '.join(individual_words)

    clean_statement = ' '.join(phrases)
    clean_statement = re.sub("[()]", ".", clean_statement)
    
    if(len(clean_statement) == 0):
        clean_statement = str(doc)
    
    return clean_statement
####################################################################################

####################################################################################

def convert_and_reduce(input_string):
    phrases_new = []
    phrases1 = []
    statement = convert_punctuation_to_dots(input_string)
    phrases = statement.split('.')

    for item in phrases:
        if("and" in item and len(get_pos(item, verbs = True)) > 1):
            phrases1.append(item)
            
        else:
            phrases1.append(sentence_reduction(item, single_phrase = True))
    
    phrases1 = list(filter(None, phrases1))
    for i in phrases1:
        phrases_new.append(i)
        
    for i in range(0,len(phrases1)):
        if(len(phrases1[i]) == 0 and phrases1[i] in phrases_new):
            phrases_new.pop(i)
    
    if(len(phrases_new) == 0):
        return '. '.join(phrases)
    
    return '. '.join(phrases_new)
##############################################################

def translate(phrase):
    clean_phrase = clean_data(phrase)
    clean_phrase = clean_phrase.replace(" a ", " ah ")
    r = requests.post(url = "https://translation.googleapis.com/language/translate/v2?key="+appglobals.config.getGoogleTranslateKey(), 
                      data = {
                              "q": clean_phrase,
                              "source" : "en",
                              "target": "hi",
                              'format': 'text'
                              })

    hindi_translation = r.json()['data']['translations'][0]['translatedText']
    
    r = requests.post(url = "https://translation.googleapis.com/language/translate/v2?key="+appglobals.config.getGoogleTranslateKey(), 
                      data = {
                              "q": hindi_translation,
                              "source" : "hi",
                              "target": "en",
                              'format': 'text'
                              })

    english_translation = r.json()['data']['translations'][0]['translatedText']
    
    return english_translation

##############################################################

def pre_escorts2(phrase):
    clean_phrase = clean_data(phrase)
    split_words = clean_phrase.split()
    for i in range(0,len(split_words)):
        if(split_words[i] == "service"):
                   break
    words = split_words[i+1 : len(split_words)]
    final_phrase = ' '.join(words)
    final_phrase = re.sub("[^a-zA-Z.,]", " ", final_phrase)
    final_phrase = final_phrase.strip()
    
    return final_phrase
    


