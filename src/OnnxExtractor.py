import json
import os
import cv2
import numpy as np
import onnxruntime
from .FaceCrop import FaceCrop
from .face_data_utils import vectorParse

class OnnxExtractor(object):
    def __init__(self,):
        self.initConfig()
        self.init()


    def initConfig(self):
        # int. Number of feature vector dimensions of face. (Don't modify it, if you don't know what it means)
        # self.face_dim = 19
        # self.eyes_dim = 13
        # self.mouth_dim = 7
        # self.nose_dim = 15
        self.face_weight_path = "weights/FDENet_face.onnx"
        self.eyes_weight_path = "weights/FDENet_eyes.onnx"
        self.mouth_weight_path = "weights/FDENet_mouth.onnx"
        self.nose_weight_path = "weights/FDENet_nose.onnx"
        self.hrnet_weight_path = "weights/HRNet.onnx"
        self.im_size = (256,256)


    def init(self):
        try:
            self.face_model_ort = onnxruntime.InferenceSession(os.path.join(os.path.abspath(os.path.dirname(__file__)),self.face_weight_path)
                                                               ,providers=['TensorrtExecutionProvider', 'CUDAExecutionProvider', "ROCMExecutionProvider", "DmlExecutionProvider",'CPUExecutionProvider'])
                                                                #  ,providers=['DmlExecutionProvider', 'CUDAExecutionProvider'])
        except:
            raise Exception("Face模型加载失败！")
        
        try:
            self.eyes_model_ort = onnxruntime.InferenceSession(os.path.join(os.path.abspath(os.path.dirname(__file__)),self.eyes_weight_path)
                                                               ,providers=['TensorrtExecutionProvider', 'CUDAExecutionProvider', "ROCMExecutionProvider", "DmlExecutionProvider",'CPUExecutionProvider'])
        except:
            raise Exception("Eyes模型加载失败！")
        try:
            self.mouth_model_ort = onnxruntime.InferenceSession(os.path.join(os.path.abspath(os.path.dirname(__file__)),self.mouth_weight_path)
                                                               ,providers=['TensorrtExecutionProvider', 'CUDAExecutionProvider', "ROCMExecutionProvider", "DmlExecutionProvider",'CPUExecutionProvider'])
                                                                #  ,providers=['DmlExecutionProvider', 'CUDAExecutionProvider'])
        except:
            raise Exception("Mouth模型加载失败！")
        
        try:
            self.nose_model_ort = onnxruntime.InferenceSession(os.path.join(os.path.abspath(os.path.dirname(__file__)),self.nose_weight_path)
                                                               ,providers=['TensorrtExecutionProvider', 'CUDAExecutionProvider', "ROCMExecutionProvider", "DmlExecutionProvider",'CPUExecutionProvider'])
        except:
            raise Exception("Nose模型加载失败！")
        
        try:
            self.hrnet_ort = onnxruntime.InferenceSession(os.path.join(os.path.abspath(os.path.dirname(__file__)),self.hrnet_weight_path)
                                                               ,providers=['TensorrtExecutionProvider', 'CUDAExecutionProvider', "ROCMExecutionProvider", "DmlExecutionProvider",'CPUExecutionProvider'])
        except:
            raise Exception("HRNet模型加载失败！")
        try:
            self.face_crop= FaceCrop()
        except:
            raise Exception("MTCNN加载失败！")
        
    
    def extract(self,filename:str,savepath:str):
        img = self.readImage(filename)
        
        try:
            faces=self.face_crop.crop(img,alignment=True)
        except:
            raise Exception("面部裁切失败！")
        
        if len(faces)==0:
            raise Exception("未检测到人脸，请更换提取图片！")
        elif len(faces)>1:
            raise Exception("检测到多张人脸，请更换提取图片！")
        
        image = self.transforms(faces[0])

        try:
            heatmap:np.ndarray=self.hrnet_ort.run(['out'], {'in':image})[0]
        except:
            raise Exception("关键点特征提取失败！")
        # eyes = face[:,:,35:70,...]
        # eyes = np.zeros_like(face)
        # eyes[:,:,35:70,...] = face[:,:,35:70,...]

        
        try:
            face_output:np.ndarray=self.face_model_ort.run(['out'], {'image': image,"heatmap":heatmap})[0].squeeze(0)
            eyes_output:np.ndarray=self.eyes_model_ort.run(['out'], {'image': image,"heatmap":heatmap})[0].squeeze(0)
            mouth_output:np.ndarray=self.mouth_model_ort.run(['out'], {'image': image,"heatmap":heatmap})[0].squeeze(0)
            nose_output:np.ndarray=self.nose_model_ort.run(['out'], {'image': image,"heatmap":heatmap})[0].squeeze(0)
            # face_output[20:32]=face_output[20:32]*weight[0] +eyes_output*weight[1]
            output=np.concatenate([face_output,eyes_output,nose_output,mouth_output])
            output=self.decode_output(output)
            data = vectorParse(output)
        except:
            raise Exception("面部数据提取失败！")
        
        try:
            with open(savepath,"w",encoding="utf-8") as f:
                json.dump(data,f,ensure_ascii=False,indent=4)
        except:
            raise Exception("面部数据写入失败！")
        
        # return True
    def decode_output(self,v:np.ndarray):
        return v*3.0-1.0
    
    
    def readImage(self, filename):
        try:
            img=cv2.imdecode(np.fromfile(filename,dtype=np.uint8),-1)
            # img = cv2.imread(filename=filename)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # img = img[:, :, [2, 1, 0]]
        except:
            raise Exception("图片读取失败！")
            
        return img
    
    def transforms(self,img:np.ndarray):
        try:
            if self.im_size is not None:
                img = cv2.resize(img, self.im_size, interpolation = cv2.INTER_AREA)
            # HWC to CHW
            img = np.transpose(img, (2,0,1))
            img = np.expand_dims(img,0).astype(np.float32)/255.0
        except:
            raise Exception("图片Transforms失败！")
        
        return img
        
if __name__ =="__main__":
    # Step 1, Create an Extractor instance
    extractor = OnnxExtractor()
    # Step 2, Extract the face data from image to json file
    data=extractor.extract(filename="test/sutaner_face.jpg",savepath="test/sutaner_face.json")
    # [Optional] Step 3, Print face data to the console
    print(data)