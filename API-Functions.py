#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 14:13:11 2018

@author: Ashwin
"""
from Functions import sentence_reduction, convert_punctuation_to_dots, convert_and_reduce        
from 
                   
def sublist(lst1, lst2):
    return set(lst1) <= set(lst2)

def validate_reduction(content):
    filters_fields = ["clean_data", "sentence_reduction", "convert_punctuation_to_dots", "convert_and_reduce"]
    keylist = content.keys()
    if("q" and "filters" not in keylist):
        return {'status' : False, 'message' : "Error: Input has a missing field(s)", "result": None}
        
    sentence = content['q']
    filters = content['filters']

    if((type(sentence) != str and type(sentence) != list) or type(filters) != list):
        return {'status' : False, 'message' : "Error: 'q' must be a string or list and 'filters' must be a list of strings", "result": None}
        
    if(sublist(filters, filters_fields) != True):
        return {'status' : False, 'message' : "Error: one or more of the mentioned filters is incorrect", "result": sentence}
    
    else:
        return {'status' : True}

def reduce(content):
    filters = content['filters']
    columns = content['q']
    filters = content['filters']

    if (type(columns)==list):
        if(len(columns) > 1):
            sentence = choose_column(columns)
        
        else:
            sentence = columns[0]
    else:
        sentence = columns

    modified_sentence = sentence
    
    for flag in filters:
        if(flag == "clean_data"):
            modified_sentence = clean_data(modified_sentence, no_numbers = True)
        elif("sentence_reduction" in filters and "convert_punctuation_to_dots" in filters):
            modified_sentence = convert_and_reduce(modified_sentence)
            break
        elif(flag == "sentence_reduction"):
            modified_sentence = sentence_reduction(modified_sentence)
        elif(flag == "convert_punctuation_to_dots"):
            modified_sentence = convert_punctuation_to_dots(modified_sentence)
        
    return {'status' : True, 'message' : "Success", 'result' : modified_sentence}
    

   
