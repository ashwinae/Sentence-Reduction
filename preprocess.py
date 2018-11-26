#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 14:13:11 2018

@author: Ashwin
"""
from preprocess.preprocess_rules import clean_data, sentence_reduction, convert_punctuation_to_dots, convert_and_reduce, translate, pre_escorts2

def choose_column(columns):
    words = ["work done", "customer call", "workdone", "call", "phone", "transfer",
             "dealer", "duplicate", "assign", "kindly", "registered", "close", "time",
             "show room", "showroom", "visit", "pay", "amount", "demand", "warranty",
             "complaint"]
    column = 0
    while (column<len(columns)):
        found = False
        if(len(columns[column]) != 0):
            for item in words:
                if(item in columns[column]):
                    found= True
                    break
            if found:
                column+=1
                continue
            else:
                return columns[column]
        column+=1
    return columns[0]
        
                   
def sublist(lst1, lst2):
    return set(lst1) <= set(lst2)

def validate_preprocess(content):
    filters_fields = ["defect", "clean_data", "sentence_reduction", "convert_punctuation_to_dots", "convert_and_reduce", "spell_check", "grammar_correction", "translate", "duplicate_removal",
                      "pre_escorts2"]
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

def preprocess(content):
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
        if(flag == "pre_escort2"):
            modified_sentence = pre_escorts2(modified_sentence)
        if(flag == "defect" and '-' in sentence):
            modified_sentence = sentence.split('-')[1]
        elif(flag == "clean_data"):
            modified_sentence = clean_data(modified_sentence, no_numbers = True)
        elif(flag == "translate"):
            modified_sentence = translate(modified_sentence)
        elif("sentence_reduction" in filters and "convert_punctuation_to_dots" in filters):
            modified_sentence = convert_and_reduce(modified_sentence)
            break
        elif(flag == "sentence_reduction"):
            modified_sentence = sentence_reduction(modified_sentence)
        elif(flag == "convert_punctuation_to_dots"):
            modified_sentence = convert_punctuation_to_dots(modified_sentence)
        
    return {'status' : True, 'message' : "Success", 'result' : modified_sentence}
    

   
