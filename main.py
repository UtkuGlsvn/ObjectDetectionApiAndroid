# @Author: utkuglsvn <glsvn>
# @Date:   2019-05-22T16:46:15+03:00
# @Last modified by:   glsvn
# @Last modified time: 2019-05-24T01:00:30+03:00
from imageai.Prediction import ImagePrediction
import os
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyBfI8eRvHW4ANVLzja6RPEn_QShqUWG9Bo",
  "authDomain": "anirec-52adc.firebaseapp.com",
  "databaseURL": "https://anirec-52adc.firebaseio.com",
  "projectId": "anirec-52adc",
  "storageBucket": "anirec-52adc.appspot.com",
  "messagingSenderId": "477126062386",
  "appId": "1:477126062386:web:7a0e0d6febd36014"
};
firebase=pyrebase.initialize_app(firebaseConfig)
storage=firebase.storage()
storage.child("images/plantImg").download("downloaded.jpg")
db=firebase.database().child("results")

prediction = ImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath(os.path.join("resnet50_weights_tf_dim_ordering_tf_kernels.h5"))
prediction.loadModel()

def swap_character(text):
    a=list(text)
    for i in range (0,len(a)):
        if a[i]=='_':
            a[i]=" "
    return ("".join(a))

#while True:
dict={}
predictions, probabilities = prediction.predictImage("downloaded.jpg", result_count=2 )
for eachPrediction, eachProbability in zip(predictions, probabilities):
    dict[eachPrediction]=eachProbability
    print(eachPrediction,":",eachProbability)

mydata=[]
for x,y in dict.items():
    data={swap_character(x):("%.2f" % y)}
    mydata.append(data)
db.set(mydata)
