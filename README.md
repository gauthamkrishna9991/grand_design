# Grand_Design



Download yolo.weights here and copy it to the integrated design folder <br/>
Download agegender model and copy it to integrated design folder.(rename it to agegender.hdf5)

[Download yolo weights](https://pjreddie.com/media/files/yolov3.weights)
[Download agegender model](https://github.com/yu4u/age-gender-estimation/releases/download/v0.5/weights.28-3.73.hdf5)

After cloning,install the require packages

```
pip install -r requirements.txt
```


To run the search engine
```
cd integrated_design
```

and 

```
python app.py
```

go to [localhost](http://127.0.0.1:5000/api) and  upload an image first (currently a vehicle or image of a person)

 
 Search samples
 ```
sample 1: test drive this <img>

sample 2: diseases this gender <img> have
```


# QUICK Tutorial

Check the files inside the integrated design folder.

## Flask app

The app.py contains a flask app.Flask is a popular, extensible web microframework for building web applications with Python.
The query from the search page is recieved by flask app and redirected to another url where processing is done.

## ElasticSearch

The elasticsearch module inside app.py creates indexes using a sitemap.xml (it is also in the same folder) and these indexes are used to get the resultant outputs for a search query. The pageranking algorithm is based on the number of words in the query appearing inside a website.

## Image classification models

The image classification models, here used are seperated into different functions, each function for each kind of image classification. The models could be found inside imagedetect.py .

## Eywa 

Eywa is a conversational agent which contains modules like Classifier,EntityExtractor, Pattern , etc and here we used an eywa classifier to sort the classes which a query belongs to.

[learn more about eywa here](https://github.com/farizrahman4u/eywa/tree/master/eywa)

## Searchwithimage

The file searchwithimage.py contains the codebase for integrated search with image and string. 

## License
This Project is Protected by the GNU Public License v3.0 (GPL 3.0).

All rights reserved as stated by [GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)


