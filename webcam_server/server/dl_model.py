import dlib
import scipy.misc
import numpy as np
import os


def main():
    # Get Face Detector from dlib
    # This allows us to detect faces in images
    face_detector = dlib.get_frontal_face_detector()

    # Get Pose Predictor from dlib
    # This allows us to detect landmark points in faces and understand the pose/angle of the face
    shape_predictor = dlib.shape_predictor(
        'server/static/models/shape_predictor_68_face_landmarks.dat')

    # Get the face recognition model
    # This is what gives us the face encodings (numbers that identify the face of a particular person)
    face_recognition_model = dlib.face_recognition_model_v1(
        'server/static/models/dlib_face_recognition_resnet_model_v1.dat')

    # This is the tolerance for face comparisons
    # The lower the number - the stricter the comparison
    # To avoid false matches, use lower value
    # To avoid false negatives (i.e. faces of the same person doesn't match), use higher value
    # 0.5-0.6 works well
    TOLERANCE = 0.6

    # This function will take an image and return its face encodings using the neural network
    def get_face_encodings(path_to_image):
        # Load image using scipy
        image = scipy.misc.imread(path_to_image)

        detected_faces = face_detector(image, 1)

        shapes_faces = [shape_predictor(image, face) for face in detected_faces]

        return [np.array(face_recognition_model.compute_face_descriptor(image, face_pose, 1)) for face_pose in
                shapes_faces]

    # This function takes a list of known faces
    def compare_face_encodings(known_faces, face):

        return np.linalg.norm(known_faces - face, axis=1) <= TOLERANCE

    def find_match(known_faces, names, face):
        # Call compare_face_encodings to get a list of True/False values indicating whether there's a match
        matches = compare_face_encodings(known_faces, face)
        # Return the name of the first match
        count = 0
        for match in matches:
            if match:
                return names[count]
            count += 1
        # Return not found if no match found
        return 'Not Found'

if __name__ == '__main__':
    main()
