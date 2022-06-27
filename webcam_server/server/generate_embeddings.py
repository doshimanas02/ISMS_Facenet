import numpy as np
import pandas as pd
from deepface import DeepFace
from keras.models import load_model
import numpy as np
import connector as c

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


def findCosineSimilarity(source_representation, test_representation):
    a = np.matmul(np.transpose(source_representation), test_representation)
    b = np.sum(np.multiply(source_representation, source_representation))
    c = np.sum(np.multiply(test_representation, test_representation))
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))


def main():

    pass
    # img_pixels_arr = np.load(
    #     r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\static\data1.pkl.npy')
    # labels_arr = np.load(
    #     r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\static\data2.pkl.npy')
    # for index, pixels, label in zip(range(len(img_pixels_arr)), img_pixels_arr, labels_arr):
    #     embedding = get_embedding(pixels)
    #     insert_statement = 'INSERT INTO face_meta (ID, IMG_NAME, EMBEDDING) VALUES (?, ?, ?)'
    #     insert_args = (index, label, embedding.tobytes())
    #     c.cursor.execute(insert_statement, insert_args)
    #
    #     for i, e in enumerate(embedding):
    #         insert_statement = 'INSERT INTO face_embeddings (FACE_ID, DIMENSION, VALUE) VALUES (?, ?, ?)'
    #         insert_args = (index, i, str(e))
    #         c.cursor.execute(insert_statement, insert_args)
    #
    # c.connection.commit()


if __name__ == '__main__':
    main()
