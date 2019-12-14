#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 23:34:42 2019

@author: abhijithneilabraham
"""

def main(query1):
    import random
    from eywa.nlu import Classifier
    from eywa.nlu import EntityExtractor    
    import cv2
    import numpy as np
    from imagedetect import detectedobj,detectage,similar
    from nltk.corpus import wordnet 

    #print(label)
    CONV_SAMPLES = {
        'vehicle'       : [ "test drive this <img> ", " cost of this <img> vehicle", "what is the mileage of this <img> vehicle",
                        "which  vehicle is this <img>" ],
        'gender'    : [ " <img> What is  the disease associated with this  gender", " Diseases <img> these gender have", "Find out the gender problems of <img> Abhijith"],
        'numberofpeople' : ['how many people in this <img> ', 'number of people in <img> ', ' <img>count the people'],
        
    }
    CLF = Classifier()
    for key in CONV_SAMPLES:
        CLF.fit(CONV_SAMPLES[key], key)
    u_query=query1
    q_class = CLF.predict(u_query)
    #print(q_class)
    #            draw_label(img, (d.left(), d.top()), label)
    
    #        cv2.imwrite("result.jpg", img)
        #label=[label]
        #print(label_list)
    searchtxt=""

    
    if q_class=='gender':
        label_list=detectage('test.jpg')
        wrd=label_list[0]
        print(label_list[0])
        synonyms = [] 
  
        for i,syn in enumerate(wordnet.synsets(wrd)): 
            if i<4:
                for l in syn.lemmas(): 
                    synonyms.append(l.name()) 
        searchtxt=str(u_query).replace('<img>',label_list[0])
        
        
    elif q_class=='vehicle':
        vehicle=detectedobj('test.jpg')
        wrd=vehicle
        synonyms = [] 
  
        for i,syn in enumerate(wordnet.synsets(wrd)): 
            if i<4:
                for l in syn.lemmas(): 
                    synonyms.append(l.name()) 
        print(vehicle)
        searchtxt=str(u_query).replace('<img>',vehicle)
    return searchtxt
        
        
        

        
#    from eywa.nlu import Pattern
#    
#    p = Pattern('[fruit: apple, banana] is my favourite fruit')  # create variable [fruit] with sample values {apple, banana}
#    
#    print(p('i like grapes'))




