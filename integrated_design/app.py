from datetime import datetime
import xml.etree.ElementTree as ET 
from flask import Flask,request,jsonify,render_template,redirect,url_for
from elasticsearch import Elasticsearch
import requests
from bs4 import BeautifulSoup
import os
from werkzeug import secure_filename
import searchwithimage as swi
# from elasticsearch_dsl import Search

app=Flask(__name__)
es = Elasticsearch()



@app.before_first_request
def init():
    indexid=['sitemaporiginal.xml']
    def indexer(file):
        tree = ET.parse(file) 
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
    for i in indexid:
        indexer(i)
    return 0      

    


# Search Items
@app.route('/api',methods=['GET','POST'])
def search():
    if request.method=='POST':
        text1=request.form['text']
        print(text1)
        text1=swi.main(text1)
        body ={
            "query": {
                "multi_match":{
                    "query": text1,
                }
            }
        }

        res = es.search(index="search-index", body=body)

        result = []
        for hits in res['hits']['hits']:
            result.append(hits['_source']['url'])

        return redirect(url_for('search_result', text=result))

    return render_template('index.html')
UPLOAD_FOLDER=""
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	

def uploader():
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'test.jpg'))

    
#    return render_template('index.html')
@app.route('/imgupload',methods=['GET','POST'])
def upload_file():
    if request.method=='POST':
        uploader()
    return redirect(url_for('search'))

#showing the content
@app.route('/', methods=['GET'])
def index():
    if request.method=='GET':
        #return "Results"
        res = es.get(index="search-index", doc_type='url', id=1)
        return jsonify(res['_source'])
    return "neigh"

#Search results
@app.route('/result')
def search_result():
    text = request.args.get('text', None)
    print(text)
    return text
    


if __name__ == "__main__":
    #init()
    try:
        app.run(debug=True)
    except:
        print('invalid search')