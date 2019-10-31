#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 23:34:42 2019

@author: abhijithneilabraham
"""

import random
from eywa.nlu import Classifier
from eywa.nlu import EntityExtractor
CONV_SAMPLES = {
    'age'       : [ "What is this person's age <img> ", "Give me the <img> age", "Find out the age of <img> Abhijith",
                    "How old <img> is Abhijith" ],
    'gender'    : [ "What is <img> this person's gender", " <img> Give me the gender", "Find out the gender of <img> Abhijith"],
    'number' : ['how many people in this <img> ', 'number of people in <img> ', ' <img> count the people']
}
CLF = Classifier()
for key in CONV_SAMPLES:
    CLF.fit(CONV_SAMPLES[key], key)
u_query="how old is this person <img>"
q_class = CLF.predict(u_query)
print(q_class)

