#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 22:04:34 2019

@author: abhijithneilabraham
"""

#from bert_serving.client import BertClient
#bc = BertClient()
#bc.encode(['First do it', 'then do it right', 'then do it better'])
from clio_lite import clio_keywords
query = "BERT"
filters = [{"range":{"year_of_article":{"gte":"2018"}}}]
keywords = clio_keywords(url=url, index=index, query=query, 
                         fields=['textBody_abstract_article','title_of_article'],
                         filters=filters)

for kw in keywords:
    print(kw) 