import cv2
from mtcnn_ort import MTCNN
import numpy as np
from skimage import transform as trans
import numpy as np




class FaceCrop():
    def __init__(self):
        self.detector = MTCNN(steps_threshold=[0.7, 0.8, 0.8])
        # self.src = np.array([
        #         [30.2946, 51.6963],
        #         [65.5318, 51.5014],
        #         [48.0252, 71.7366],
        #         [33.5493, 92.3655],
        #         [62.7299, 92.2041]], dtype=np.float32)
        self.src = np.array([
                [30.2946, 51.6963],
                [65.5318, 51.5014],
                [48.0252, 71.7366],
                [33.5493, 92.3655],
                [62.7299, 92.2041]], dtype=np.float32)
        self.src[:, 0] += 16
        # self.src[:,1] += 8



    def crop(self,image:np.ndarray,crop_size:int=224,margin:int=16, alignment=True):
        '''
            image : (h,w,c) RGB
        '''

        faces = []
        if alignment:
            landmark5 = self.detector.detect_faces_raw(image)[1]
            if landmark5.size==0:
                return []
            elif landmark5.size>10:
                return [0,0]
            
            landmark5=landmark5.reshape(2, 5).T
            tform = trans.SimilarityTransform()
            tform.estimate(landmark5, self.src*2)
            M = tform.params[0:2, :]
            face = cv2.warpAffine(image, M, (crop_size+margin*2, crop_size+margin*2),borderValue=0)
            # eyes = face[40:65,...]
            faces.append(face)
            # cv2.imwrite("result.jpg", cv2.cvtColor(face, cv2.COLOR_RGB2BGR))
        else:
            result = self.detector.detect_faces(image)
            for item in result:
                bounding_box = item["box"]
                face:np.ndarray=image[bounding_box[1]-margin:bounding_box[1] + bounding_box[3]+margin,\
                        bounding_box[1]-margin:bounding_box[0]-margin,:]
                faces.append(face)
            # cv2.imwrite("result.jpg", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        return faces

