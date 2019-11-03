# grand_design



Download yolo.weights here and copy it to the booking service folder. <br/>
Download agegender.hdf5 and copy it to booking_service folder.(rename it to agegender.hdf5)

[Download yolo weights](https://pjreddie.com/media/files/yolov3.weights)
[Download agegender model](https://github.com/yu4u/age-gender-estimation/releases/download/v0.5/weights.28-3.73.hdf5)


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
