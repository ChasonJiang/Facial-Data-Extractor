import os
import subprocess
import base64
import json
from typing import Dict, List, Union

import cv2
import msgpack
import numpy as np

from .chara_loader.AiSyoujyoCharaData import AiSyoujyoCharaData

now_dir = os.path.dirname(os.path.abspath(__file__))


PROGRAM_PATH = os.path.join(now_dir, "MsgToJson", "HS2ABMX.exe")


META_DATA_LIST= [
    # (name, (min, max, length_min, length_max), has_length)
    # ('cf_J_FaceBase', (0, 2, 0.1, 5), True), 
    # ('cf_J_Head_s', (0, 2, 0, 1), False), 
    
    ('cf_J_FaceLow_s', (0, 2, 0, 1), False), 
    ('cf_J_FaceUp_ty', (0, 2, 0, 1), False), 
    ('cf_J_FaceUp_tz', (0, 2, 0, 1), False), # length?
    
    # ("cf_J_EarBase_s_L", (0, 3, 0, 1), False),
    # ("cf_J_EarBase_s_R", (0, 3, 0, 1), False),
    # ("cf_J_EarUp_L", (0, 4, 0, 1), False), 
    # ("cf_J_EarUp_R", (0, 4, 0, 1), False), 
    # ("cf_J_EarLow_L", (0, 4, 0, 1), False),
    # ("cf_J_EarLow_R", (0, 4, 0, 1), False),

    ('cf_J_Chin_rs', (0, 3, 0.1, 2), True), 
    ('cf_J_ChinLow', (0, 3, 0, 1), False), 
    ('cf_J_ChinTip_s', (0, 3, 0, 1), False), 

    ('cf_J_CheekUp_L', (0, 2, 0, 1), False), 
    ('cf_J_CheekUp_R', (0, 2, 0, 1), False), 
    ('cf_J_CheekLow_L', (0, 2, 0.1, 2.5), True), 
    ('cf_J_CheekLow_R', (0, 2, 0.1, 2.5), True), 

    # ('cf_J_Mayu_L', (0, 5, 0, 1), False), 
    # ('cf_J_Mayu_R', (0, 5, 0, 1), False), 
    # ('cf_J_MayuMid_s_L', (0, 5, 0, 1), False), 
    # ('cf_J_MayuMid_s_R', (0, 5, 0, 1), False), 
    # ('cf_J_MayuTip_s_L', (0, 5, 0, 1), False), 
    # ('cf_J_MayuTip_s_R', (0, 5, 0, 1), False), 

    ('cf_J_Eye_s_L', (0, 1.5, 0, 1), False), 
    ('cf_J_Eye_s_R', (0, 1.5, 0, 1), False), 

    ("cf_J_Eye01_s_L" , (0, 3, 0, 1), False),
    ("cf_J_Eye01_s_R" , (0, 3, 0, 1), False),
    ("cf_J_Eye02_s_L" , (0, 3, 0, 1), False),
    ("cf_J_Eye02_s_R" , (0, 3, 0, 1), False),
    ("cf_J_Eye03_s_L" , (0, 3, 0, 1), False),
    ("cf_J_Eye03_s_R" , (0, 3, 0, 1), False),
    ("cf_J_Eye04_s_L" , (0, 3, 0, 1), False),
    ("cf_J_Eye04_s_R" , (0, 3, 0, 1), False),

    ('cf_J_NoseBase_trs', (0, 2, 0, 1), False), 
    ('cf_J_NoseBase_s', (0, 2, 0, 1), False), 
    ('cf_J_Nose_tip', (0, 3, 0.1, 2.5), True), 
    ('cf_J_NoseBridge_t', (0, 2, 0, 1), False), 

    ('cf_J_MouthBase_tr', (0, 2, 0, 1), False), 
    ('cf_J_MouthMove', (0, 2, 0, 1), False), 
    ('cf_J_Mouth_L', (0, 6, 0, 1), False), 
    ('cf_J_Mouth_R', (0, 6, 0, 1), False), 
    ('cf_J_Mouthup', (0, 6, 0, 1), False), 
    ('cf_J_MouthLow', (0, 6, 0, 1), False)
    ]


REVERSE_MASK={
        "scale": [1, 1, 1],
        "position": [-1, 1, 1],
        "rotation": [1, -1, -1]
}

BONE_NAME_LIST = [item[0] for item in META_DATA_LIST]
# BONE_NAME_LIST_WITHOUT_RIGHT = [item[0] for item in META_DATA_LIST if not item[0].endswith("_R")]

META_DATA_TABLE={}
# META_DATA_TABLE_WITHOUT_RIGHT={}
for item in META_DATA_LIST:
    META_DATA_TABLE[item[0]] = (item[1], item[2])
    # if not item[0].endswith("_R"):
    #     META_DATA_TABLE_WITHOUT_RIGHT[item[0]]=(item[1], item[2])


with open(os.path.join(now_dir, "parameter_flags.json"), "r", encoding="utf-8") as f:
    PARAMETER_FLAG_TABLE = json.load(f)

PARAMETER_FLAGS = [1]*54

for key in BONE_NAME_LIST:
    for type_name in ["scale", "length", "position", "rotation"]:
        item = PARAMETER_FLAG_TABLE[key][type_name]
        if type_name!="length":
            PARAMETER_FLAGS.append(item["x"])
            PARAMETER_FLAGS.append(item["y"])
            PARAMETER_FLAGS.append(item["z"])
        else:
            PARAMETER_FLAGS.append(item)

# PARAMETER_FLAGS_WITHOUT_RIGHT = [1]*54

# for key in BONE_NAME_LIST_WITHOUT_RIGHT:
#     for type_name in ["scale", "length", "position", "rotation"]:
#         item = PARAMETER_FLAG_TABLE[key][type_name]
#         if type_name!="length":
#             PARAMETER_FLAGS_WITHOUT_RIGHT.append(item["x"])
#             PARAMETER_FLAGS_WITHOUT_RIGHT.append(item["y"])
#             PARAMETER_FLAGS_WITHOUT_RIGHT.append(item["z"])
#         else:
#             PARAMETER_FLAGS_WITHOUT_RIGHT.append(item)


with open(os.path.join(now_dir, "statistical_face_data.json"), "r", encoding="utf-8") as f:
    STATISTICAL_FACE_DATA = json.load(f)
STATISTICAL_DATA = {int(key):value for key, value in STATISTICAL_FACE_DATA.items()}
# STATISTICAL_DATA_WITHOUT_RIGHT = {int(key):value for key, value in STATISTICAL_FACE_DATA.items()}

with open(os.path.join(now_dir, "statistical_bone_data.json"), "r", encoding="utf-8") as f:
    STATISTICAL_BONE_DATA = json.load(f)

# WITHOUT_RIGHT_INDEX = []
ONLY_RIGHT_INDEX = []
ONLY_LEFT_INDEX = []
counter = 54
for key in BONE_NAME_LIST:
    for type_name in ["scale", "length", "position", "rotation"]:
        item = STATISTICAL_BONE_DATA[key][type_name]
        if type_name!="length":
            STATISTICAL_DATA[counter] = item["x"]

            if key.endswith("_L"):
                ONLY_LEFT_INDEX.append(counter)
                ONLY_RIGHT_INDEX.append(counter+10)

            counter+=1
            STATISTICAL_DATA[counter] = item["y"]

            if key.endswith("_L"):
                ONLY_LEFT_INDEX.append(counter)
                ONLY_RIGHT_INDEX.append(counter+10)
            counter+=1
            STATISTICAL_DATA[counter] = item["z"]
            # if key in BONE_NAME_LIST_WITHOUT_RIGHT:
            #     STATISTICAL_DATA_WITHOUT_RIGHT[counter] = item["z"]
            #     WITHOUT_RIGHT_INDEX.append(counter)
            if key.endswith("_L"):
                ONLY_LEFT_INDEX.append(counter)
                ONLY_RIGHT_INDEX.append(counter+10)
            counter+=1
        else:
            STATISTICAL_DATA[counter] = item
            # if key in BONE_NAME_LIST_WITHOUT_RIGHT:
            #     STATISTICAL_DATA_WITHOUT_RIGHT[counter] = item
            #     WITHOUT_RIGHT_INDEX.append(counter)
            if key.endswith("_L"):
                ONLY_LEFT_INDEX.append(counter)
                ONLY_RIGHT_INDEX.append(counter+10)
            counter+=1



def deserialize(data: bytes, version:int=2)->dict:
    encoded_data = base64.b64encode(data).decode('utf-8')
    command = [PROGRAM_PATH, "1", str(version) ,encoded_data]
    result = subprocess.run(command, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)

    # 解析C#程序返回的JSON输出
    response = json.loads(result.stdout)

    if response['status'] == True:
        data = base64.b64decode(response["data"])
        data = msgpack.unpackb(data)
    else:
        raise Exception(response['exception']+"\n"+response['msg'])

    return data

def serialize(data:list)->bytes:
    data = msgpack.packb(data, use_single_float=True)
    # data = json.dumps(data, ensure_ascii=False).encode('utf-8')
    # encoded_data = data
    encoded_data = base64.b64encode(data).decode('utf-8')
    command = [PROGRAM_PATH, "2", "2", encoded_data]
    result = subprocess.run(command, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)

    # 解析C#程序返回的JSON输出
    response = json.loads(result.stdout)

    if response['status'] == True:
        data = base64.b64decode(response["data"])
    else:
        raise Exception(response['exception']+"\n"+response['msg'])

    return data

class ABData:
    name:str = None
    length:float = 1.0
    rotation:list = [0.0, 0.0, 0.0]
    position:list = [0.0, 0.0, 0.0]
    scale:list = [1.0, 1.0, 1.0]

    def __init__(self, data:Union[list, dict, np.ndarray]=None, name:str=None, denormalize:bool=False):
        self.name = name
        if data is not None:
            if isinstance(data, list):
                self.init_from_data(data)
            elif isinstance(data, dict):
                self.init_from_dict(data)
            elif isinstance(data, np.ndarray):
                self.init_from_vector(data, name, denormalize)
            else:
                raise TypeError("Unsupported data type")
    
    def init_from_data(self, data:list):
        self.name:str = data[0]
        self.scale:list = data[1][0][0]
        self.length:float = data[1][0][1]
        self.position:list = data[1][0][2]
        self.rotation:list = data[1][0][3]

    def init_from_dict(self, data:dict):
        self.name:str = data["name"]
        self.scale:list = data["scale"]
        self.length:float = data["length"]
        self.position:list = data["position"]
        self.rotation:list = data["rotation"]
    
    def init_from_vector(self, vector:np.ndarray, name:str=None, denormalize:bool=False):

        self.scale:list = vector[:3].tolist() if not denormalize else self.denormalize(vector[:3], META_DATA_TABLE[name][0][0], META_DATA_TABLE[name][0][1]).tolist()
        self.length:float = vector[3] if not denormalize else self.denormalize(vector[3], 0, META_DATA_TABLE[name][0][-1] if META_DATA_TABLE[name][1] else 1)
        self.position:list = vector[4:7].tolist() if not denormalize else self.denormalize(vector[4:7], -1, 1).tolist()
        self.rotation:list = vector[7:10].tolist() if not denormalize else self.denormalize(vector[7:10], -180, 180).tolist()

    

    def to_dict(self)->dict:
        return {
                    "name": self.name,
                    "scale": self.scale,
                    "length": self.length,
                    "position": self.position,
                    "rotation": self.rotation
                }
    
    def to_vector(self, normalize:bool=False)->np.ndarray:
        
        if normalize:
            scale = self.normalize(np.array(self.scale), META_DATA_TABLE[self.name][0][0], META_DATA_TABLE[self.name][0][1])
            length = self.normalize(np.array([self.length]), 0, META_DATA_TABLE[self.name][0][-1] if META_DATA_TABLE[self.name][1] else 1)
            position = self.normalize(np.array(self.position), -1, 1)
            rotation = self.normalize(np.array(self.rotation), -180, 180)
            vector = np.concatenate([scale, length, position, rotation])
        else:
            vector = np.array([*self.scale, float(self.length), *self.position, *self.rotation])
        return vector.astype(np.float32)
    
    def to_list(self)->list:
        return [self.name, [[[float(item) for item in self.scale], float(self.length), [float(item) for item in self.position], [float(item) for item in self.rotation]]]]
    

    def normalize(self, vector:np.ndarray, min_value:float, max_value:float)->np.ndarray:
        return (vector - min_value) / (max_value - min_value) 
    
    def denormalize(self, vector:np.ndarray, min_value:float, max_value:float)->np.ndarray:
        return vector * (max_value - min_value) + min_value
    
    @classmethod
    def deserialize(self, raw_data:bytes, version:int=2)->List["ABData"]:
        data = deserialize(raw_data, version)

        abdatas = []
        for bone_data in data:
            abdata = ABData(bone_data)
            abdatas.append(abdata)
        return abdatas
    
    @classmethod
    def serialize(self, abdatas:List["ABData"])->bytes:
        data = [abdata.to_list() for abdata in abdatas]
        return serialize(data)


    def reset(self):
        self.length:float = 1
        self.rotation:list = [0, 0, 0]
        self.position:list = [0, 0, 0]
        self.scale:list = [1, 1, 1]
        return self

class FaceData:
    base_data:list = None
    ab_data:Dict[str, ABData] = None
    card_data:AiSyoujyoCharaData = None

    def __init__(self, file_path:str, contains_png:bool=True):
        self.file_path = file_path
        self.card_data = AiSyoujyoCharaData.load(file_path, contains_png)
        self.base_data = self.card_data.Custom["face"]["shapeValueFace"][:54] # without ear data
        try:
            abm_version = self.card_data.KKEx["KKABMPlugin.ABMData"][0]
            abm_data = self.card_data.KKEx["KKABMPlugin.ABMData"][1]["boneData"]
            ab_data = ABData.deserialize(abm_data, abm_version)
        except:
            ab_data = []
        
        self.modified_ab_keys:list = []

        # 过滤出有用的AB数据，并补充缺失的AB数据
        keys = list(META_DATA_TABLE.keys())
        self.ab_data = {}
        for item in ab_data:
            if item.name in keys:
                self.ab_data[item.name] = item
                keys.remove(item.name)
                self.modified_ab_keys.append(item.name)
        if len(keys) > 0:
            for key in keys:
                self.ab_data[key]=ABData(name=key)


    def to_vector(self, is_simplify:bool=False, without_right:bool=False, normalize:bool=False, use_gaussian:bool=True)->np.ndarray:
        base_vector = np.array(self.base_data, dtype=np.float32)
        ab_vectors = [self.ab_data[key].to_vector(False) for key in BONE_NAME_LIST]


        vector =  np.concatenate([base_vector, *ab_vectors]).astype(np.float32)
        
        statistical_data = STATISTICAL_DATA
       
        flag_mask = self._get_flag_mask(is_simplify, without_right)

        vector_ = []
        for i in range(vector.shape[0]):
            if flag_mask[i] == 1:
                if normalize:
                    if use_gaussian:
                        mean = statistical_data[i]["mean"]
                        std = statistical_data[i]["std"]
                        value = self.normalize2(vector[i], mean, std)
                    else:
                        min_value = statistical_data[i]["min"]
                        max_value = statistical_data[i]["max"]
                        value = self.normalize1(vector[i], min_value, max_value)
                else:
                    value = vector[i]
                vector_.append(value)
        vector = np.array(vector_).astype(np.float32)

        return vector
    

    
    def _get_flag_mask(self, is_simplify:bool=False, without_right:bool=False)->list:
        mask = [1]*(len(BONE_NAME_LIST)*10+54)
        for idx in range(len(BONE_NAME_LIST)*10+54):
            if idx in ONLY_RIGHT_INDEX and without_right:
                mask[idx] = 0
            if PARAMETER_FLAGS[idx]==0 and is_simplify:
                mask[idx] = 0
        return mask
    
    def _get_reverse_mask(self,)->list:
        mask = [1.0]*54+[1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, -1.0, -1.0]*len(BONE_NAME_LIST)
        return mask


    def normalize1(self, value:float, min_value:float, max_value:float)->np.ndarray:
        if (max_value - min_value)==0:
            raise ZeroDivisionError("max_value - min_value cannot be zero")
        return (value - min_value) / (max_value - min_value) 
            
        
    def denormalize1(self, value:float, min_value:float, max_value:float)->np.ndarray:
        return value * (max_value - min_value) + min_value
    
    def normalize2(self, vector:np.ndarray, mean:float, std:float)->np.ndarray:
        if std == 0:
            raise ZeroDivisionError("std cannot be zero")
        return (vector - mean) / std

    
    def denormalize2(self, vector:np.ndarray, mean:float, std:float)->np.ndarray:
        return vector * std + mean
    
    def set_from_vector(self, vector:np.ndarray, is_simplify:bool=False, without_right:bool=False, denormalize:bool=False, use_gaussian:bool=True):

        flag_mask = self._get_flag_mask(is_simplify, without_right)
        reverse_mask = self._get_reverse_mask()
        statistical_data = STATISTICAL_DATA
        vector_ = self.to_vector(False, False )
        counter = 0
        
        for i in range(vector_.shape[0]):
            if flag_mask[i]==1:
                if denormalize:
                    if use_gaussian:
                        mean = statistical_data[i]["mean"]
                        std = statistical_data[i]["std"]
                        vector_[i] = self.denormalize2(vector[counter], mean, std) 
                        if without_right and (i in ONLY_LEFT_INDEX):
                            vector_[i+10] = vector_[i]*reverse_mask[i+10]
                    else:
                        min_value = statistical_data[i]["min"]
                        max_value = statistical_data[i]["max"]
                        vector_[i] = self.denormalize1(vector[counter], min_value, max_value)
                        if without_right and (i in ONLY_LEFT_INDEX):
                            vector_[i+10] = vector_[i]*reverse_mask[i+10]
                else:
                    vector_[i] = vector[counter]
                    if without_right and (i in ONLY_LEFT_INDEX):
                        vector_[i+10] = vector_[i]*reverse_mask[i+10]
                counter+=1

        vector = vector_.astype(np.float32)
        base_vector = vector[:54]
        self.base_data = base_vector.tolist()
        for i, key in enumerate(BONE_NAME_LIST):
            if key in self.ab_data:
                self.ab_data[key].init_from_vector(vector[54+i*10:54+(i+1)*10], key, False)
            else:
                self.ab_data[key] = ABData(name=key, vector=vector[54+i*10:54+(i+1)*10], denormalize=False)
    
    def set_image(self, image:np.ndarray):
        # ( h, w, 3) RGB
        assert image.ndim == 3
        # print(image.shape)
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        _,image=cv2.imencode(".png",image)
        image = image.tobytes()
        self.card_data.image = image


    def save(self, path:str=None)->bytes:
        if path is None:
            path = self.file_path
        ab_data = [abdata.to_list() for abdata in self.ab_data.values()]
        ab_data = serialize(ab_data)
        self.card_data.Custom["face"]["shapeValueFace"][:54] = self.base_data
        self.card_data.KKEx["KKABMPlugin.ABMData"] = [2, {"boneData": ab_data}]
        self.card_data.save(path)


