import pickle
import cv2
# import face_recognition
import os
import warnings
from deepface import DeepFace


warnings.filterwarnings("ignore")


# def predict(rgb_frame, knn_clf=None, model_path=None, distance_threshold=0.3):
#     if knn_clf is None and model_path is None:
#         raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")
#
#     # Load a trained KNN model (if one was passed in)
#     if knn_clf is None:
#         with open(model_path, 'rb') as f:
#             knn_clf = pickle.load(f)
#
#         # Load image file and find face locations
#         # X_img = face_recognition.load_image_file(X_img_path)
#     X_face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=2)
#
#     # If no faces are found in the image, return an empty result.
#     if len(X_face_locations) == 0:
#         return []
#
#         # Find encodings for faces in the test iamge
#     faces_encodings = face_recognition.face_encodings(rgb_frame, known_face_locations=X_face_locations)
#
#     # Use the KNN model to find the best matches for the test face
#     closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=5)
#     are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
#     # print(closest_distances)
#     # Predict classes and remove classifications that aren't within the threshold
#     return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in
#             zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]


# def predict_pic(frame):
#     # Resize frame of video to 1/4 size for faster face recognition processing
#     frame = cv2.imread(frame)
#     # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#     #
#     # # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
#     # rgb_frame = small_frame[:, :, ::-1]
#
#     predictions = predict(frame, model_path="server/static/models/trained_model.clf")
#
#     return predictions


def predict_adv(frame):

    path = os.path.join(os.getcwd() + r'\server\static\images\dataset')
    print(frame)
    for dir in os.listdir(os.path.join(path)):
        print(os.path.join(path, dir))
        df = DeepFace.find(img_path=frame, db_path=os.path.join(path, dir), enforce_detection=False)
        if not df.empty:
            vgg_cosine_list = df['VGG-Face_cosine'].tolist()
            print(min(vgg_cosine_list))
            if min(vgg_cosine_list) < 0.2:
                return dir

    return 'unknown'


def detect_face(frame):
    file_path = frame
    frame = cv2.imread(frame)
    face = DeepFace.detectFace(frame, enforce_detection=False)
    detected_face = face * 255
    cv2.imwrite(file_path, detected_face[:, :, ::-1])

# def retrieve_data(adhar):
#     if adhar != 'unknown':
#         print(adhar)
#     else:
#         print(adhar)
#
#
# def main():
#     path = 'C:/Users/darvik07/Desktop/Server Today/webcam_server/server/static/images/temp/'
#     for file in os.listdir(path):
#         file_path = str(path)+str(file)
#         predictions = predict_pic(file_path)
#         adhar = predictions[0][0]
#         retrieve_data(adhar)
#
#
# if __name__ == "__main__":
#     main()