import numpy as np
import pandas as pd
from deepface import DeepFace
from keras.models import load_model
import numpy as np
import sqlite3

model = load_model(
    r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\static\models\facenet_keras.h5')


def get_embedding(face_pixels):
    # scale pixel values
    face_pixels = face_pixels.astype('float32')
    # standardize pixel values across channels (global)
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    # transform face into one sample
    samples = np.expand_dims(face_pixels, axis=0)
    # make prediction to get embedding
    yhat = model.predict(samples)
    return yhat[0]


def load_and_execute(face_array, label_array):
    connection = sqlite3.connect(
        r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\database\facialdb.db')
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    for pixels, label in zip(face_array, label_array):
        embedding = get_embedding(pixels)
        insert_statement = 'INSERT INTO face_meta (IMG_NAME, EMBEDDING) VALUES (?, ?)'
        insert_args = (label, embedding.tobytes())
        cursor1.execute(insert_statement, insert_args)
        id = cursor1.lastrowid
        for i, e in enumerate(embedding):
            insert_statement = 'INSERT INTO face_embeddings (FACE_ID, DIMENSION, VALUE) VALUES (?, ?, ?)'
            insert_args = (id, i, str(e))
            cursor2.execute(insert_statement, insert_args)

    connection.commit()


def main():
    pass
    # img_pixels_arr = np.load(
    #     r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\static\data1.pkl.npy')
    # labels_arr = np.load(
    #     r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\static\data2.pkl.npy')



if __name__ == '__main__':
    main()
