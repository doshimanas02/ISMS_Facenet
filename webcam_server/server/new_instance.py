import os
from .process_dataset import process
import numpy as np
from .detect_faces_dlib import dlib_corrected
from .generate_embeddings import load_and_execute
from PIL import Image


def add_new_instance(adharno_path):
    data = process(adharno_path)
    face_np_array, face_np_label = dlib_corrected(data)
    load_and_execute(face_np_array, face_np_label)
    print('Inserted new entries to DB')


def main():
    pass


if __name__ == "__main__":
    main()