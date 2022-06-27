import os
import pickle
import pandas as pd
import numpy as np
from PIL import Image


path = "C:/Users/Administrator/Datasets/lfw"

def main():
    data = pd.DataFrame(columns=['img', 'class'])
    for dir in os.listdir(path):
        print('Processing ' + dir)
        for file in os.listdir(path + '/' + dir):
            np_array = create_array_from_image(path + '/' + dir + '/' + file)
            data = data.append({'img':np_array, 'class':dir}, ignore_index=True)
    return data


def create_array_from_image(file_path):
    image = Image.open(file_path)
    np_array = np.asarray(image)
    return np_array


if  __name__ == "__main__":
    data = main()
    data.to_pickle('C:/Users/Administrator/Datasets/lfw_faces.pkl')

