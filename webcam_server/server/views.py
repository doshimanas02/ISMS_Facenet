import os

from .models import Face
from .prediction import predict_adv, detect_face
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from pybase64 import b64decode
import time
import json
from django.http import JsonResponse
from collections import defaultdict
import requests

@csrf_exempt
def process_image(request):
    user_list = list()
    path = 'server/static/images/temp/'
    if request.method == 'POST':
        # print(request.POST.getlist('data[]'))
        for i in range(5):
            img_data = request.POST[f'photo{i}']
            # print(img_data)
            format, imgstr = img_data.split(';base64,')
            file_path = f"{path}{time.strftime('%Y%m%d-%H%M%S')}'m'{i}.png"
            with open(file_path, 'wb') as f:
                f.write(b64decode(imgstr))
            detect_face(file_path)
            predictions = predict_adv(file_path)
            user = retrieve_data(predictions)
            if user['Name'] != 'unknown':
                for fi in os.listdir(path):
                    file_path = str(path) + str(fi)
                    os.remove(file_path)
                return HttpResponse(json.dumps(user), content_type="application/json")

    for f in os.listdir(path):
        file_path = str(path) + str(f)
        os.remove(file_path)

    unknown_dict = defaultdict()
    unknown_dict['Name'] = 'unknown'
    unknown_dict['Rank'] = 'unknown'
    unknown_dict['Number'] = 'unknown'
    unknown_dict['Adhar'] = 'unknown'
    unknown_dict['Cat'] = 'unknown'
    unknown_dict['gender'] = 'unknown'
    unknown_dict['B'] = 'unknown'
    unknown_dict['snumber'] = 'unknown'

    return HttpResponse(json.dumps(unknown_dict), content_type="application/json")


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
