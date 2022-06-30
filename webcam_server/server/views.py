import datetime
import os
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pybase64 import b64decode
import time
import json, io
from collections import defaultdict
from .predict_target import predict
from .new_instance import add_new_instance
from PIL import Image
from .models import Face, Save
from django.db.models import Q

@csrf_exempt
def process_image(request):
    path = r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\static\temp'
    if request.method == 'POST':
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


@csrf_exempt
def get_with_aadhaar(request):
    aadhar_no = request.POST['aadhaar']
    data = retrieve_data(aadhar_no)
    if data['Name'] != 'unknown':
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return HttpResponse('unknown')


@csrf_exempt
def add_data(request):
    path = "C:/Users/Administrator/Datasets/dataset"
    if request.method == 'POST':
        name = request.POST['name']
        rank = request.POST['rank']
        number = request.POST['number']
        aadhar = request.POST['aadhar']
        blacklist = request.POST['blacklist']
        category = request.POST['category']
        gender = request.POST['gender']
        snumber = request.POST['snumber']
        date = datetime.datetime.now().date()
        time = datetime.datetime.now().time()
        username = 'Dhairya'

        print(blacklist, category, gender)
        data = Face(name=name, rank=rank, number=number, adharno=aadhar, blacklist=blacklist, cat=category,
                      gender=gender, snumber=snumber, date=date, time=time, username=username)
        # try:
        #     original_umask = os.umask(0o777)
        #     os.mkdir(f'C:/Users/Administrator/Datasets/dataset/{aadhar}')
        # except PermissionError or FileExistsError:
        #     print("Permission denied or File already exists")
        #     exit(1)
        # for i in range(5):
        #     img_data = request.POST[f'photo{i}']
        #     format, imgstr = img_data.split(';base64,')
        #     imgstr = b64decode(imgstr)
        #     with open(dest_path + '/' + f"photo{i}.png", "wb") as fh:
        #         fh.write(imgstr)
        #
        # add_new_instance(adharno_path=dest_path)
        # data.save()
        return HttpResponse("success")
    return HttpResponse("Failed!: POST request expected")

@csrf_exempt
def entry(request):
    if request.POST['val'] == 'In':
        aadhar = request.POST['aadhar']
        person = Save.objects.filter(adharno=aadhar).last()
        # print(type(person.dateout))
        if (person and person.dateout is not None) or not person:
            name = request.POST['name']
            rank = request.POST['rank']
            number = request.POST['number']
            blacklist = request.POST['blacklist']
            category = request.POST['category']
            gender = request.POST['gender']
            snumber = request.POST['snumber']
            token = request.POST['token']
            datein = datetime.datetime.now().date()
            timein = datetime.datetime.now().time()

            add_to_db = Save(name=name, rank=rank, number=number, adharno=aadhar, blacklist=blacklist, cat=category,
                          snumber=snumber, datein=datein, timein=timein, token=token)
            add_to_db.save()
            return HttpResponse('Ingress recorded successfully.')
        else:
            return HttpResponse('The system has not yet recorded the person\'s egress. Please record the same to continue. ')

    if request.POST['val'] == 'Out':
        aadhar = request.POST['aadhar']
        person_data = Save.objects.filter(adharno=aadhar, dateout=None).last()
        if person_data:
            person_data.timeout = datetime.datetime.now().time()
            person_data.dateout = datetime.datetime.now().date()
            person_data.save()
            return HttpResponse('Egress recorded successfully.')
        else:
            return HttpResponse(
                'The system has not yet recorded the person\'s ingress. Please record the same to continue. ')

    return HttpResponse('Invalid Request')


def index(request):
    # print("BOBO")
    return render(request, 'index.html')

