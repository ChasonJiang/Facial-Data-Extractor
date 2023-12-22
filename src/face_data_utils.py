import numpy as np
import cv2

from .chara_loader import AiSyoujyoCharaData, KoikatuCharaData

FACE_DATA_FIELD = [
    # 整体
    "全脸宽度",
    "脸上部前后位置",
    "脸部上方和下方",
    "下脸前后位置",
    "脸下部宽度",
    # 下巴
    "下颚宽度",
    "下巴上下位置1",
    "下巴前后位置",
    "下颚角度",
    "下颚底部上下位置",
    "下巴宽度",
    "下巴上下位置2",
    "下巴前后",
    # 脸颊
    "脸颊下部上下位置",
    "下颊前后",
    "下颊宽度",
    "脸颊上部上下位置",
    "上颊前后",
    "脸上部宽度",
    # 眼
    "眼睛上下",
    "眼位",
    "眼睛前后",
    "眼宽1",
    "眼宽2",
    "眼角z轴",
    "眼角y轴",
    "左右眼位置1",
    "左右眼位置2",
    "眼角上下位置1",
    "眼角上下位置2",
    "眼皮形状1",
    "眼皮形状2",
    # 鼻子
    "整个鼻子上下位置",
    "整个鼻子前后",
    "鼻子整体角度X轴",
    "鼻子的整个宽度",
    "鼻梁高度",
    "鼻梁宽度",
    "鼻梁形状",
    "鼻宽",
    "上下鼻子",
    "鼻子前后",
    "机头角度X轴",
    "机头角度Z轴",
    "鼻子高度",
    "鼻尖X轴",
    "鼻尖大小",
    # 嘴唇
    "嘴上下",
    "口宽",
    "嘴唇宽度",
    "嘴前后位置",
    "上嘴唇形",
    "下嘴唇形",
    "嘴型嘴角",
    # 耳
    "耳长",
    "耳角Y轴",
    "耳角Z轴",
    "上耳形",
    "耳下部形状",
    # 其他
    "眉色",
    "唇色",
    "眼影颜色",
    "腮红颜色",
]

def vectorParse(vector:np.ndarray)->dict:
    
    assert isinstance(vector,np.ndarray)
    # assert len(vector) -12 == len(FACE_DATA_FIELD)
    
    data = {}
    index = 0
    for i in range(len(FACE_DATA_FIELD)):
        field = FACE_DATA_FIELD[i]
        if index == len(vector):
            break
        if field not in ["眉色","唇色","眼影颜色","腮红颜色"]:
            data[field] = round(vector[index]*100)
            index+=1
        else:
            rgba= [round(idx*255) for idx in vector[index:index+3]]
            rgba.append(round(vector[index+3]*100))
            data[field]=rgba
            index+=4
        
    return data

def vectorToChara(vector:np.ndarray,save_path:str,template_chara_path:str,image:np.ndarray=None,chara_class:str="AIS"):
    assert chara_class in ["AIS","KK"]
    assert isinstance(vector,np.ndarray)
    assert isinstance(image,np.ndarray) or image==np.ndarray
    
    if image is not None:
        # ( h, w, 3)
        assert image.ndim == 3
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        _,image=cv2.imencode(".png",image)
        image = image.tobytes()

    if chara_class=="AIS":
        chara=AiSyoujyoCharaData.load(template_chara_path)
    elif chara_class == "KK":
        chara=KoikatuCharaData.load(template_chara_path)

    chara.image = image
    chara["Custom"]["face"]["shapeValueFace"][:54]=vector.astype(np.float32).tolist()

    chara.save(save_path)