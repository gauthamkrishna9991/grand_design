#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:35:16 2019

@author: abhijithneilabraham
"""

from nltk.corpus import wordnet 
wrd="bag"
#this can be used for semantics 
#syns = wordnet.synsets(wrd)
# 
#  
## An example of a synset: 
#print(syns[0].name()+" name") 
#  
## Just the word: 
#print(syns[0].lemmas()[0].name()+" lemmas") 
#  
## Definition of that first synset: 
#print(syns[0].definition()+" definition") 
#  
## Examples of the word in use in sentences: 
#print(syns[0].examples()) 
import nltk 
from nltk.corpus import wordnet 
synonyms = [] 
  
for i,syn in enumerate(wordnet.synsets(wrd)): 
    if i<4:
        for l in syn.lemmas(): 
            synonyms.append(l.name()) 

  
print(list(set(synonyms)))
