#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 12:17:59 2019

@author: abhijithneilabraham
"""
text="test drive this car"
from nltk.tokenize import word_tokenize
tokenized_word=word_tokenize(text)
print(tokenized_word)
from nltk.probability import FreqDist
fdist = FreqDist(tokenized_word)
print(fdist.most_common)