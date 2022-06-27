import os
import pickle

import cv2
from sklearn import neighbors
import face_recognition

save_path = 'server/static/images/dataset/'
model_save_path = 'server/static/models/'

def train_model():
    X = []
    y = []
    for dir in os.listdir(save_path):
        for file in os.listdir(save_path + dir):
            image = face_recognition.load_image_file(save_path+dir+"/"+file)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                print("Image {} not suitable for training: {}".format(file, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                # Add face encoding for current image to the training set
                X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(dir.split('_')[0])

    # knn_clf = neighbors.KNeighborsClassifier(n_neighbors=None, algorithm='ball_tree', weights='distance')
    # knn_clf.fit(X, y)

    # Save the trained KNN classifier
    # with open(model_save_path, 'wb') as f:
    #     pickle.dump(knn_clf, f)
    #
    # return knn_clf

def detect_face(image):
    face_data = list()
    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), None, 0)
        roi_color = image[y:y + h, x:x + w]
        face_data.append(roi_color)

    return face_data

def main():
    i = 0
    path = 'server/static/dataset/'
    for dir in os.listdir(path):
        os.mkdir(save_path+dir)
        for file in os.listdir(path + "/" + dir):
            faces = detect_face(path + "/" + dir + "/" + file)
            for face in faces:
                print("[INFO] Object found. Saving locally.")
                cv2.imwrite(f'{save_path+dir+"/"}{i}_detected.jpg', face)
                i += 1

    model = train_model()

