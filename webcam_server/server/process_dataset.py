import os
import pickle
import pandas as pd
import numpy as np
from PIL import Image


def process(aadhaar_dir):
    data = pd.DataFrame(columns=['img', 'class'])
    for file in os.listdir(aadhaar_dir):
        np_array = create_array_from_image(aadhaar_dir + '/' + file)
        data = data.append({'img': np_array, 'class': aadhaar_dir}, ignore_index=True)
    return data


def create_array_from_image(file_path):
    image = Image.open(file_path)
    np_array = np.asarray(image)
    return np_array


if  __name__ == "__main__":
    pass
