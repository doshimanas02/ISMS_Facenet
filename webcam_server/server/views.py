import os
from .models import Face
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pybase64 import b64decode
import time
import json, io
from collections import defaultdict
from .predict_target import predict
from PIL import Image
from .process_request import process_requested_img

@csrf_exempt
def process_image(request):
    path = r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\static\temp'
    if request.method == 'POST':
        # print(request.POST.getlist('data[]'))
        for i in range(5):
            img_data = request.POST[f'photo{i}']
            format, imgstr = img_data.split(';base64,')
            imgstr = b64decode(imgstr)
            image = Image.open(io.BytesIO(imgstr))
            prediction = predict(image)[0]
            if prediction != 'u':
                user = retrieve_data(prediction)
                return HttpResponse(json.dumps(user), content_type="application/json")

    return HttpResponse("unknown")


def retrieve_data(adhar):
    udata = defaultdict()
    print(adhar)
    if adhar != 'unknown':
        try:
            data = Face.objects.get(adharno=adhar)
            udata['Name'] = data.name
            udata['Rank'] = data.rank
            udata['Number'] = data.number
            udata['Adhar'] = data.adharno
            udata['Cat'] = data.cat
            udata['gender'] = data.gender
            udata['B'] = data.blacklist
            udata['snumber'] = data.snumber
            return udata
        except:
            pass
    udata['Name'] = 'unknown'
    udata['Rank'] = 'unknown'
    udata['Number'] = 'unknown'
    udata['Adhar'] = 'unknown'
    udata['Cat'] = 'unknown'
    udata['gender'] = 'unknown'
    udata['B'] = 'unknown'
    udata['snumber'] = 'unknown'
    return udata


def index(request):
    # print("BOBO")
    return render(request, 'index.html')

