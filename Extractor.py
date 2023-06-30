import json
import os
import cv2
import numpy as np
import onnxruntime
from face_data_utils import vectorParse

class Extractor(object):
    def __init__(self,):
        self.initConfig()
        self.init()

    def initConfig(self):
        # int. Number of feature vector dimensions of face. (Don't modify it, if you don't know what it means)
        self.num_dim = 59
        # to extract on "cpu" or "cuda"(gpu)
        # self.device = torch.device("cuda")
        # string.saveing path of model
        self.model_load_path = "models\\resnet34_head_1_epoch_30_with_colorjitter.onnx"
        # tuple. resize image to the shape. The aspect ratio should be 9:16
        # self.im_size = (252, 352)
        self.im_size = None


    def init(self):

        # self.model = torchvision.models.resnet34(pretrained=True)
        # self.model.fc = torch.nn.Linear(self.model.fc.in_features, self.num_dim)
        # if self.model_load_path is not None:
        #     self.load_model(self.model_load_path,self.model,False)
        # self.model=self.model.to(self.device)
        try:
            
            self.ort_session = onnxruntime.InferenceSession(os.path.join(os.path.abspath(os.path.dirname(__file__)),self.model_load_path))
        except:
            raise Exception("模型加载失败！")

        
    def extract(self,filename:str,savepath:str):
        img = self.readImage(filename)
        try:
            output:np.ndarray=self.ort_session.run(['out'], {'in': img})[0]
            data = vectorParse(output.squeeze(0))
            data = json.dumps(data,ensure_ascii=False,indent=4)
        except:
            raise Exception("面部数据提取失败！")
        
        try:
            with open(savepath,"w",encoding="utf-8") as f:
                f.write(data)
        except:
            raise Exception("面部数据写入失败！")

        # return True

    def readImage(self, filename):
        try:
            img=cv2.imdecode(np.fromfile(filename,dtype=np.uint8),-1)
            # img = cv2.imread(filename=filename)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # img = img[:, :, [2, 1, 0]]
            if self.im_size is not None:
                img = cv2.resize(img, self.im_size, interpolation = cv2.INTER_AREA)
            # HWC to CHW
            img=np.transpose(img, (2,0,1))
            img= np.expand_dims(img,0).astype(np.float32)/255.0
        except:
            raise Exception("图片读取失败！")
            
        return img


if __name__ =="__main__":
    # Step 1, Create an Extractor instance
    extractor = Extractor()
    # Step 2, Extract the face data from image to json file
    data=extractor.extract(filename="test/dlrb.jpg",savepath="test/dlrb.json")
    # [Optional] Step 3, Print face data to the console
    print(data)