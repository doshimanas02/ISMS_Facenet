from facenet_pytorch import MTCNN
from matplotlib import pyplot as plt
from PIL import Image
import torch
import os
from numpy import asarray
import cv2
import numpy as np

mtcnn = None


def init_mtcnn():
    global mtcnn
    # create the detector, using default weights
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    mtcnn = MTCNN(select_largest=False, device=device, post_process=False)


# extract a single face from a given photograph
def extract_face(file_path, dir, parent_dir, file_name):
    # load image from file
    frame = cv2.imread(file_path)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)

    # Detect face
    mtcnn(frame, save_path=parent_dir + '/LFW_Faces/' + dir + '/' + file_name)


# boxes, probs, landmarks = mtcnn.detect(frame, landmarks=True)


# # Visualize
# fig, ax = plt.subplots(figsize=(16, 12))
# ax.imshow(frame)
# ax.axis('off')
#
# for box, landmark in zip(boxes, landmarks):
# 	ax.scatter(*np.meshgrid(box[[0, 2]], box[[1, 3]]))
# 	ax.scatter(landmark[:, 0], landmark[:, 1], s=8)
# fig.show()

def main():
    init_mtcnn()
    path = 'D:/WhitespaceVoid/Projects/Datasets'
    for dir in os.listdir(path + '/LFW/'):
        print('Processing ' + dir)
        for file in os.listdir(path + '/LFW/' + dir):
            extract_face(path + '/LFW/' + dir + '/' + file, dir, path, file)


if __name__ == '__main__':
    main()
