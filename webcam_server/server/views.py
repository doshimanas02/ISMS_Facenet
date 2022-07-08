import datetime
import os
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pybase64 import b64decode
import time
import json, io
from .predict_target import predict, predict_all
from .new_instance import add_new_instance
from PIL import Image
from .models import Face, Save
from .retrieve_data import retrieve_data
import shutil


@csrf_exempt
def process_image(request):
    path = r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\static\temp'
    if request.method == 'POST':
        images = []
        for i in range(5):
            img_data = request.POST[f'photo{i}']
            format, imgstr = img_data.split(';base64,')
            imgstr = b64decode(imgstr)
            image = Image.open(io.BytesIO(imgstr))
            result = predict(image)[0]
            data = retrieve_data(result)
            if data == 'u':
                continue
            else:
                return HttpResponse(json.dumps(data), content_type="application/json")
            # images.append(image)
    return HttpResponse("unknown")


@csrf_exempt
def get_with_aadhaar(request):
    aadhar_no = request.POST['aadhaar']
    data = retrieve_data(aadhar_no)
    if data != 'unknown' and data['Name'] != 'unknown':
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
        username = 'Nirma_CSE'

        # print(blacklist, category, gender)
        data = Face(name=name, rank=rank, number=number, adharno=aadhar, blacklist=blacklist, cat=category,
                      gender=gender, snumber=snumber, date=date, time=time, username=username, picclick=False)
        try:
            try:
                if Face.objects.get(adharno=aadhar):
                    return HttpResponse('User Details already exist in the database.')
            except:
                pass
            original_umask = os.umask(0o777)
            os.mkdir(f'C:/Users/Administrator/Datasets/dataset/{aadhar}')
            for i in range(5):
                img_data = request.POST[f'photo{i}']
                format, imgstr = img_data.split(';base64,')
                imgstr = b64decode(imgstr)
                with open(f'C:/Users/Administrator/Datasets/dataset/{aadhar}' + '/' + f"photo{i}.png", "wb") as fh:
                    fh.write(imgstr)
            if add_new_instance(adharno_path=f'C:/Users/Administrator/Datasets/dataset/{aadhar}') == -1:
                raise
            data.save()
            return HttpResponse("success")
        except Exception as ex:
            dirpath = f'C:/Users/Administrator/Datasets/dataset/{aadhar}'
            if os.path.exists(dirpath) and os.path.isdir(dirpath):
                os.system('rmdir /S /Q "{}"'.format(dirpath))
            return HttpResponse('Some error occured when entering database. Error as follows: ', ex)
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
            # print("Token: ", token)
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

@csrf_exempt
def newentry(request):
    return render(request, "Form.html")
