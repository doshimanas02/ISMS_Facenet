import os
from .process_dataset import process
import numpy as np
from .detect_faces_dlib import dlib_corrected, dlib_deepface
from .generate_embeddings import load_and_execute
from PIL import Image
from random import randint
import shutil

aadhar = set()
path2 = r"C:\Users\Administrator\Datasets\lfw"


def random_with_N_digits(n = 12):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return str(randint(range_start, range_end))


def add_new_instance(adharno_path):
    data = process(adharno_path)
    face_np_array, face_np_label = dlib_deepface(data)
    load_and_execute(face_np_array, face_np_label)
    print('Inserted new entries to DB')


def make_dir_fail_safe(path, folder):
    try:
        shutil.copytree(path2 + '\\' + folder, path)
        return True
    except Exception:
        return False


def main():
    path = r'C:/Users/Administrator/Datasets/dataset/'
    add_new_instance(path + '918800518581')
    # for folder in os.listdir(path):
    #     add_new_instance(path + folder)



if __name__ == "__main__":
    main()