import os
from process_dataset import process
from detect_faces_dlib import dlib_corrected
from generate_embeddings import load_and_execute


def add_new_instance(adharno):
    # create dataframe containing image pixel array to label mapping
    print('Processing ', adharno)
    data = process(adharno)
    # data.to_pickle(r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\static\temp_dataset.pkl')
    # detect faces from pixels
    face_np_array, face_np_label = dlib_corrected(data)
    load_and_execute(face_np_array, face_np_label)
    print('Inserted new entries to DB')


def main():
    path = "C:/Users/Administrator/Datasets/dataset"
    for dir in os.listdir(path):
        add_new_instance(dir)


if __name__ == "__main__":
    main()