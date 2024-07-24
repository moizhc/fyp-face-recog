from PIL import Image
from skimage import transform as trans 
import numpy as np
import os
import cv2
# from mtcnn_pytorch.src.align_trans import get_reference_facial_points, warp_and_crop_face

class FaceAligner:
    def __init__(self, detector, desiredFaceWidth=112, 
                 desiredFaceHeight=None):
        self.detector = detector
        self.desiredFaceWidth = desiredFaceWidth
        self.desiredFaceHeight = desiredFaceHeight
        # if the desired face height is None, set it to be the
        # desired face width (normal behavior)
        if self.desiredFaceHeight is None:
            self.desiredFaceHeight = self.desiredFaceWidth

    def align(self, image):
        # print("Align function called")
        image=np.array(image)
        aligned_faces = []
        landmarks, bbox, _ = self.detector(image)
        # print("Align function called  2")

        if not landmarks:
            return None, None, None
        img= np.array(image)
        landmarks = np.array(landmarks).reshape(-1, 2)
        # print("Detected landmarks:", landmarks)

        ref_landmarks = np.array([[38.29459953, 51.69630051],
                                    [73.53179932, 51.50139999],
                                    [56.02519989, 71.73660278],
                                    [41.54930115, 92.3655014 ],
                                    [70.72990036, 92.20410156]])
        # print("Align function called  bf similartity")
        # print("refrence  landmarks:",  ref_landmarks)

        tform = trans.SimilarityTransform()
        # print("Align function called  af similartity")

        tform.estimate(landmarks, ref_landmarks)
        # print(tform.params)
               


        tfm = tform.params[0:2, :]     
        # print("Transformation matrix shape before vstack:", tfm.shape)
        # print("Transformation matrix before vstack:", tfm)
        
        tfm = np.vstack([tfm, [0, 0, 1]])

        # print("Transformation matrix after vstack:", tfm)
        # print("Transformation matrix shape after vstack:", tfm.shape)

        output = cv2.warpAffine(img, tfm[:2, :], (self.desiredFaceWidth, self.desiredFaceHeight))
        
        aligned_faces_array = np.array(output)


        return Image.fromarray(aligned_faces_array)
    
    def align_multi(self, image):
        aligned_faces = []
        landmarks, bbox, _ = self.detector(image)

        if not landmarks:
            return None, None, None

        landmarks = np.array(landmarks)  # Convert landmarks to a NumPy array

        for landmark in landmarks:
            ref_landmarks = np.array([[38.29459953, 51.69630051],
                                    [73.53179932, 51.50139999],
                                    [56.02519989, 71.73660278],
                                    [41.54930115, 92.3655014 ],
                                    [70.72990036, 92.20410156]])
            tform = trans.SimilarityTransform()
            tform.estimate(landmark, ref_landmarks)
            tfm = tform.params[0:2, :]
            tfm = np.vstack([tfm, [0, 0, 1]])
            output = cv2.warpAffine(image, tfm[:2, :], (self.desiredFaceWidth, self.desiredFaceHeight))
            aligned_faces.append(output)
            

        return aligned_faces, landmarks, bbox
    
