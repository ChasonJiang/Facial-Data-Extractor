import os
import cv2
import numpy as np
import onnxruntime
from .face_data_utils.FaceCrop import FaceCrop
from .face_data_utils.utils import FaceData
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE" 
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))




class Extractor(object):
    def __init__(self,):
        self.initConfig()
        self.init()


    def initConfig(self):
        self.weight_path = os.path.join(CURRENT_DIR, "weights", "model.onnx")
        self.providers = ["CUDAExecutionProvider", "DmlExecutionProvider", "CPUExecutionProvider"]


    def init(self):
        try:
            self.ort_session = onnxruntime.InferenceSession(self.weight_path, providers=self.providers)
        except:
            raise RuntimeError("Failed to load onnx model")

        self.face_crop = FaceCrop()
        
        
    def extract(self, image_path:str, save_dir:str, template_path:str, use_face_detector=True):
        os.makedirs(save_dir, exist_ok=True)
        face = self.process_image(image_path, use_face_detector)

        output=self.ort_session.run(['vector'], {'image': face})[0][0]
        
        face_data = FaceData(template_path)
        face_data.set_from_vector(output, is_simplify=True, without_right=True, denormalize=True, use_gaussian=False)
        
        # face_image = np.zeros([313, 224, 3], dtype=np.float32)

        face_image = np.pad(face.squeeze(0).transpose(1,2,0)*255,((44,45), (0,0), (0,0)), mode='constant', constant_values=0)
        face_data.set_image(face_image)
        

        
        save_path = os.path.join(save_dir, os.path.basename(image_path).split('.')[0] + '_character.png')
        face_data.save(save_path)
        return output
    
    



    def process_image(self, file_path:str, use_face_detector=True, im_size=(224,224)):
        img=cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if use_face_detector:
            faces = self.face_crop.crop(img)
            if len(faces)==0:
                raise RuntimeError("没有检测到人脸，请更换图片！")
            if len(faces)>1:
                raise RuntimeError("检测到多个人脸，请更换图片！")
            face = faces[0]
        else:
            face = img
        if face.shape[0]!= im_size[0] or face.shape[1]!= im_size[1]:
            face = cv2.resize(face, im_size, interpolation = cv2.INTER_AREA)
        # HWC to CHW
        face_np=np.transpose(face, (2,0,1)).astype(np.float32)/255
        face_np=np.expand_dims(face_np,axis=0)
        
        return face_np
    
if __name__ =="__main__":
    # Step 1, Create an Extractor instance
    extractor = Extractor()
    # Step 2, Extract the face data from image to json file
    image_path = r"visualization\123.jpg"
    save_dir = "visualization"
    template_path = r"src\assets\template.png"
    use_face_detector = True
    data=extractor.extract(image_path=image_path, save_dir=save_dir, template_path=template_path, use_face_detector=use_face_detector)
    # [Optional] Step 3, Print face data to the console
    print(data)