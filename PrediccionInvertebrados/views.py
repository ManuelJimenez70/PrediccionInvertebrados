import numpy as np
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.utils import shuffle
import os
from PIL import Image
import keras_tuner as kt
from tensorflow import keras as kr
import os
from django.http import HttpResponse
from django.template import Context, Template
from django.views.decorators.csrf import csrf_protect
from PrediccionInvertebrados.settings import BASE_DIR
## tiempo que se tarda en predecir
from keras.layers import BatchNormalization
from keras.models import load_model
from django import forms
from django.views.decorators.csrf import csrf_exempt

  
model = load_model("PrediccionInvertebrados/static/models/model.h5", custom_objects={"BatchNormalization": kr.layers.BatchNormalization})

def predict():
    
    test_image = kr.preprocessing.image.load_img("PrediccionInvertebrados/static/images/predict.jpg", target_size=(100,100))
    test_image = kr.preprocessing.image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict(test_image, verbose=0)

    mx_value = max(result[0])
    if result[0][0] == mx_value:
        tho = 'arachnid'
    elif result[0][1] == mx_value:
        tho = 'insect'
    elif result[0][2] == mx_value:
        tho = 'centipede'
    elif result[0][3] == mx_value:
        tho = 'crustacean'

    return [tho, str(round(result[0][0]*100,2)), str(round(result[0][1]*100,2)), str(round(result[0][2]*100,2)), str(round(result[0][3]*100,2))]

class MyForm(forms.Form):
    image = forms.FileField(label="image")
  

myform = MyForm()

@csrf_exempt
def save_image(request):
    if request.method == "POST":
        imagepp = request.FILES["imagep"]
        imagefile = Image.open(imagepp)
        imagefile.save("PrediccionInvertebrados/static/images/predict.jpg")
        result = predict()

        doc = open((os.path.join(BASE_DIR, "PrediccionInvertebrados/templates/result.html")))
        template = Template(doc.read())
        doc.close()
        context = Context({"result": result[0], "arachnid": result[1], "insect": result[2], "centipede": result[3], "crustacean": result[4]})
        document = template.render(context)
        return HttpResponse(document)
    
    return index(request)
    
def index(request):
    doc = open((os.path.join(BASE_DIR, "PrediccionInvertebrados/templates/index.html")))
    template = Template(doc.read())
    doc.close()
    context = Context()
    document = template.render(context)
    return HttpResponse(document)
