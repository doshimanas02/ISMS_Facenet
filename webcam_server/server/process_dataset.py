import os
import pickle
import pandas as pd
import numpy as np
from PIL import Image


path = "C:/Users/Administrator/Datasets/dataset"

def process(dir):
    data = pd.DataFrame(columns=['img', 'class'])
    for file in os.listdir(path + '/' + dir):
        np_array = create_array_from_image(path + '/' + dir + '/' + file)
        data = data.append({'img':np_array, 'class':dir}, ignore_index=True)
    return data


def create_array_from_image(file_path):
    image = Image.open(file_path)
    np_array = np.asarray(image)
    return np_array


if  __name__ == "__main__":
    pass
    # for
    # data = process()
    # data.to_pickle(r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\static\dataset.pkl')

