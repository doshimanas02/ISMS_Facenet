import os
from collections import defaultdict
from .models import Face
from pybase64 import b64decode, b64encode
from PIL import Image

path = 'C:/Users/doshi/Datasets/dataset/'
def retrieve_data(adhar):
    udata = defaultdict()
    # print(adhar)
    if adhar != 'unknown':
        try:
            data = Face.objects.get(adharno=adhar)
            # print('Here')
            udata['Name'] = data.name
            udata['Rank'] = data.rank
            udata['Number'] = data.number
            udata['Adhar'] = data.adharno
            udata['Cat'] = data.cat
            udata['gender'] = data.gender
            udata['B'] = data.blacklist
            udata['snumber'] = data.snumber
            udata['token'] = data.token
            with open(path + adhar + '/' + (os.listdir(path + adhar))[0], 'rb') as f:
                udata['image'] = b64encode(f.read()).decode('ascii')
            return udata
        except:
            pass
    udata = 'unknown'
    return udata