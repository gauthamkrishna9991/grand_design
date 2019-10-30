from datetime import datetime
import xml.etree.ElementTree as ET 
from flask import Flask,request,jsonify,render_template,redirect,url_for
from elasticsearch import Elasticsearch
import requests
from bs4 import BeautifulSoup
# from elasticsearch_dsl import Search

app=Flask(__name__)
es = Elasticsearch()



@app.before_first_request
def init():
    tree = ET.parse('sitemap.xml') 
    root = tree.getroot()
    id=0 

    for url in root.findall('url'):
        link = url.find('loc').text
        # linkTemp= link.split('/')
        text=""
        print(link)
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html5lib')
        # print(soup.find('a'))

        # for i in linkTemp:
        #     text+= i+" "
        # print(text)
        body={
            "url":link,
            "text": str(soup),
        }
        
        es.index(index="search-index",doc_type='url',id=id,body=body)  
        id+=1
        print(link)
    return 0      


    

# Search Items
@app.route('/',methods=['GET','POST'])
def search():
    if request.method=='POST':
        text=request.form['text']
        body ={
            "query": {
                "multi_match":{
                    "query": text,
                }
            }
        }

        res = es.search(index="search-index", body=body)
        print(res)

        result = []
        print(".................STONKS ............")
        for hits in res['hits']['hits']:
            print(hits['_source']['url'])
            result.append(hits['_source']['url'])
            print(result)
        
        return redirect(url_for('search_result', text=result))

    return render_template('index.html')

#showing the content
@app.route('/api', methods=['POST'])
def index():
    if request.method=='POST':
        txt=""
        #return "Results"
        
#        for i in range(5):
#            res = es.get(index="search-index", doc_type='url', id=i)
#            txt+=' \n '+str(res['_source']['url'])
        i=0
        try:
            while es.get(index="search-index", doc_type='url', id=i):
                res=es.get(index="search-index", doc_type='url', id=i)
                txt+=' \t '+str(res['_source']['url'])
                i+=1
        except :
            print('end of search')
            
#        print(res['_source'])
        return '<html> '+txt+' </html>'




    


if __name__ == "__main__":
    # init()
    app.run(debug=True)