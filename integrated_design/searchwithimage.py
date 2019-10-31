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
    'age'       : [ "Diseases associated with this age <img> ", "<img> Give me the  problems of this age", "Find out the happiness at this age of <img> Abhijith",
                    "How old <img> is Abhijith when he have blood sugar" ],
    'gender'    : [ " <img> What is  disease associated with this  gender", " Diseases <img> these gender have", "Find out the gender problems of <img> Abhijith"],
    'number' : ['how many people in this <img> ', 'number of people in <img> ', ' <img>count the people']
}
CLF = Classifier()
for key in CONV_SAMPLES:
    CLF.fit(CONV_SAMPLES[key], key)
u_query="age related disease of <img>"
q_class = CLF.predict(u_query)
print(q_class)

