import os
import pickle
import pandas as pd
import numpy as np
from PIL import Image


def main():
    data = pd.DataFrame(columns=['img', 'class'])
    path = "D:/WhitespaceVoid/Projects/Datasets/LFW"
    for dir in os.listdir(path):
        print('Processing ' + dir)
        for file in os.listdir(path + '/' + dir):
            image = Image.open(path + '/' + dir + '/' + file)
            np_array = np.asarray(image)
            data = data.append({'img':np_array, 'class':dir}, ignore_index=True)
    return data

if  __name__ == "__main__":
    # data = main()
    # data.to_csv('D:/WhitespaceVoid/Projects/Datasets/data.pkl')
    data = pd.read_pickle('D:/WhitespaceVoid/Projects/Datasets/data.pkl')
    # data = pd.read_csv('D:/WhitespaceVoid/Projects/Datasets/data.csv', dtype=np.array)
    # print(data.head(10))
    print(type(data['img'][0]))


