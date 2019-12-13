##!/usr/bin/env python3
## -*- coding: utf-8 -*-
#"""
#Created on Fri Dec 13 22:31:38 2019
#
#@author: abhijithneilabraham
#"""
#
#from eywa.math import vector_sequence_similarity,euclid_distance,get_token_score,euclid_similarity
#from eywa.lang import Document
#
#x=Document('king')
#x=x.embeddings
#
#y=Document('queen')
#y=y.embeddings
#import numpy
#
#
#import spacy
#import wmd
#
#nlp = spacy.load('en')
##nlp.add_pipe(wmd.WMD.SpacySimilarityHook(nlp), last=True)
#doc1 = nlp("cat")
#doc2 = nlp("banana bag")
#print(doc1.similarity(doc2))
#
##print(doc1.similarity(doc2))
#
## Program to measure similarity between  
## two sentences using cosine similarity. 
#from nltk.corpus import stopwords 
#from nltk.tokenize import word_tokenize 
#  
## X = input("Enter first string: ").lower() 
## Y = input("Enter second string: ").lower() 
#X ="I love horror movies"
#Y ="Lights out is a horror movie"
#  
## tokenization 
#X_list = word_tokenize(X)  
#Y_list = word_tokenize(Y) 
#  
## sw contains the list of stopwords 
#sw = stopwords.words('english')  
#l1 =[];l2 =[] 
#  
## remove stop words from string 
#X_set = {w for w in X_list if not w in sw}  
#Y_set = {w for w in Y_list if not w in sw} 
#  
## form a set containing keywords of both strings  
#rvector = X_set.union(Y_set)  
#for w in rvector: 
#    if w in X_set: l1.append(1) # create a vector 
#    else: l1.append(0) 
#    if w in Y_set: l2.append(1) 
#    else: l2.append(0) 
#c = 0
#  
## cosine formula  
#for i in range(len(rvector)): 
#        c+= l1[i]*l2[i] 
#cosine = c / float((sum(l1)*sum(l2))**0.5) 
#print("similarity: ", cosine)
import spacy 
  
nlp = spacy.load('en_core_web_sm') 
  
print("Enter two space-separated words") 
words = input() 
  
tokens = nlp(words) 
  
for token in tokens: 
    # Printing the following attributes of each token. 
    # text: the word string, has_vector: if it contains 
    # a vector representation in the model,  
    # vector_norm: the algebraic norm of the vector, 
    # is_oov: if the word is out of vocabulary. 
    print(token.text, token.has_vector, token.vector_norm, token.is_oov) 
  
token1, token2 = tokens[0], tokens[1] 
  
print("Similarity:", token1.similarity(token2)) 
