import deepface.DeepFace
import numpy as np
import dlib
import cv2
import pandas as pd
from deepface import DeepFace
from facenet_pytorch import MTCNN
import os
from PIL import Image

detector = dlib.cnn_face_detection_model_v1(
    r"C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\static\models\mmod_human_face_detector.dat")


def rect_to_bb(rect):
    # take a bounding predicted by dlib and convert it
    # to the format (x, y, w, h) as we would normally do
    # with OpenCV
    x = rect.rect.left()
    y = rect.rect.top()
    w = rect.rect.right() - x
    h = rect.rect.bottom() - y

    # return a tuple of (x, y, w, h)
    return x, y, w, h


def dlib_corrected(data, data_type='train'):
    # We set the size of the image
    dim = (160, 160)
    data_images = []
    # If we are processing training data we need to keep track of the labels
    if data_type == 'train':
        data_labels = []
    # Loop over all images
    for cnt in range(0, len(data)):
        print('Processing ', cnt)
        image = data['img'][cnt]
        # The large images are resized
        gray = pre_process(image)
        # Detect the faces
        rects = detector(gray, 1)
        sub_images_data = []
        # If no face is detected in the image we will add a NaN
        if len(rects) == 0:
            if data_type == 'train':
                sub_images_data = np.empty(dim + (3,))
                sub_images_data[:] = np.nan
            if data_type == 'test':
                nan_images_data = np.empty(dim + (3,))
                nan_images_data[:] = np.nan
                sub_images_data.append(nan_images_data)
        else:
            sub_images_data = process_faces(image, rects, dim, data_type)
        # Here we add the image(s) to the list we will return
        data_images.append(sub_images_data)
        # And add the label to the list
        if data_type == 'train':
            data_labels.append(data['class'][cnt])
    # Lastly we need to return the correct number of arrays
    if data_type == 'train':
        return np.array(data_images), np.array(data_labels)
    else:
        return np.array(data_images)


def dlib_deepface(data, data_type="train"):
    dim = (160, 160)
    data_images = []
    # If we are processing training data we need to keep track of the labels
    if data_type == 'train':
        data_labels = []
    for cnt in range(0, len(data)):
        print('Processing ', cnt)
        image = data['img'][cnt]
        backends = ['opencv', 'ssd', 'dlib', 'mtcnn']
        detected_face = DeepFace.detectFace(image, detector_backend='dlib', enforce_detection=False)
        all_zeros = not np.any(detected_face)
        sub_images_data = []
        if all_zeros:
            if data_type == 'train':
                sub_images_data = np.empty(dim + (3,))
                sub_images_data[:] = np.nan
            if data_type == 'test':
                nan_images_data = np.empty(dim + (3,))
                nan_images_data[:] = np.nan
                sub_images_data.append(nan_images_data)
        else:
            rgbImg = cv2.resize(detected_face, dim, interpolation=cv2.INTER_AREA)
            sub_images_data = rgbImg.copy()

        data_images.append(sub_images_data)
        # And add the label to the list
        if data_type == 'train':
            data_labels.append(data['class'][cnt])
        # Lastly we need to return the correct number of arrays
    if data_type == 'train':
        return np.array(data_images), np.array(data_labels)
    else:
        return np.array(data_images)


def pre_process(image):
    if image.shape[0] > 1000 and image.shape[1] > 1000:
        image = cv2.resize(image, (1000, 1000), interpolation=cv2.INTER_AREA)
    # The image is converted to grey-scales
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray


def process_faces(image, rects, dim, data_type='train'):
    sub_images_data = []
    # Loop over all faces in the image
    for (i, rect) in enumerate(rects):
        # Convert the bounding box to edges
        (x, y, w, h) = rect_to_bb(rect)
        # Here we copy and crop the face out of the image
        clone = image.copy()
        if x >= 0 and y >= 0 and w >= 0 and h >= 0:
            crop_img = clone[y:y + h, x:x + w]
        else:
            crop_img = clone.copy()
        # We resize the face to the correct size
        rgbImg = cv2.resize(crop_img, dim, interpolation=cv2.INTER_AREA)
        # In the test set we keep track of all faces in an image
        sub_images_data = rgbImg.copy()
        # if data_type == 'train':
        #     sub_images_data = rgbImg.copy()
        # else:
        #     sub_images_data.append(rgbImg)
    return sub_images_data


def main():
    path = 'C:/Users/Administrator/PycharmProjects/ISMS_DeepFace/webcam_server/server'
    data = pd.read_pickle(path + '/static/dataset.pkl')
    # print(data['class'])
    arr1, arr2 = dlib_corrected(data)
    np.save(path + '/static/data1.pkl', arr=arr1)
    np.save(path + '/static/data2.pkl', arr=arr2)


if __name__ == "__main__":
    main()
