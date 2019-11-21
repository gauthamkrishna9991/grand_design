#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 01:05:45 2019

@author: abhijithneilabraham
"""

import requests
import json

def make_query(url, q, alg, field, shard_size=1000, size=25):
    """See this gist for docs"""
    query = {"query" : { "match" : {field : q } },
             "size": 0,
             "aggregations" : {
                 "my_sample" : {
                     "sampler" : {"shard_size" : shard_size},
                     "aggregations": {
                        "keywords" : {
                            "significant_text" : {
                                "size": size,
                                "field" : field,
                                alg:{}
                             }
                        }
                    }
                }
            }
        }
    return [row['key'] 
            for row in requests.post(f'{url}/_search',
                                     data=json.dumps(query),
                                     headers={'Content-Type':'application/json'}).json()['aggregations']['my_sample']['keywords']['buckets']]
# Make the initial vanilla query
r = simple_query(url, old_query, event, fields)
data, docs = extract_docs(r)
# Formulate the MLT query
total = data['hits']['total']
max_doc_freq = int(max_doc_frac*total)
min_doc_freq = int(min_doc_freq*total)
mlt_query = {"query":
             {"more_like_this":
              {"fields": fields,  # the fields to consider
               "like": docs,  # the seed docs
               "min_term_freq": min_term_freq,
               "max_query_terms": max_query_terms,
               "min_doc_freq": min_doc_freq,
               "max_doc_freq": max_doc_freq,
               "boost_terms": 1.,
               "minimum_should_match": minimum_should_match,
               "include": True  # include the seed docs
              }
             }
            }
# Make the MLT query
query = json.dumps(dict(**query, **mlt_query))
params = {"search_type":"dfs_query_then_fetch"}
r_mlt = requests.post(url, data=query,
                      headers=headers,
                      params=params)
# Extract the results
_data, docs = extract_docs(r_mlt)