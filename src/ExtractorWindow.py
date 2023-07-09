import json
import os
import traceback
from .Extractor import Extractor
from PyQt5.QtCore import QUrl,pyqtSignal
from PyQt5.QtWidgets import QWidget,QFileDialog
from .ExtractorWindow_UI import Ui_Extractor
from .Processor import Processor 
from .VersionChecker import VersionChecker

class ExtractorWindow(QWidget,Ui_Extractor):
    chekversion_signal = pyqtSignal()
    def __init__(self, parent: QWidget | None=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        
        self.openBtn.clicked.connect(self.openImage)
        self.extractBtn.clicked.connect(self.process)
        self.img_path = None
        self.save_path = None
        self.extractor=None
        self.version="1.1.0"
        self.hello()
        self.chekversion_signal.connect(self.checkVersion)
        self.chekversion_signal.emit()
    #     self.loadExtractor()
        
        
    def checkVersion(self):
        self.log("正在检查更新...")
        vc=VersionChecker()
        vc.result_signal.connect(self.printVersionInfo)
        vc.finished.connect(lambda:vc.result_signal.disconnect())
        vc.start()
        
    def printVersionInfo(self,info:dict):
        if not info["State"]:
            self.log(info["msg"])
            return
        
        if self.version == info["Version"]:
            self.log("已是最新版本！\n")
        else:
            self.log(f"检测到新版本: {info['Version']}\n")
            self.log(f"更新日志: \n{info['UpdateInfo']}")
            self.log(f"访问以下链接下载更新：\n\tgithub: {info['Download']['Github']}\n\t百度网盘: {info['Download']['BaiduNetDisk']}\n")
            self.log("-----------------------------------------------------------------------------------\n")
        
        
    def loadExtractor(self,):
        if self.extractor is not None:
            return True
        
        try:
            self.extractor = Extractor()
        except:
            self.log(traceback.format_exc())
            self.log("Extractor 加载失败！\n")
            return False
        
        self.log("Extractor 加载成功！\n")
        return True
    
    def hello(self,):
        self.log(f'''
\t\t欢迎使用 Facial Data Extractor

    本软件利用AI从人物图像中提取人脸数据，用于辅助Illusion系列游戏中的人物捏脸。
    目前，只支持 AI Shoujo 和 Honey Select2。
    
    作者：ChasonJiang
    Github：https://github.com/ChasonJiang/Face-Data-Extractor
    当前版本：{self.version}

使用教程:
    Step1. 点击“打开图片”按钮, 选择图片。
    Step2. 点击“提取”按钮, 等待提取面部数据。
    Step3. 使用记事本或任意编辑器，打开提取完毕的json文件。

注意事项：
    1. 脸型可以使用官方的三种脸型，“类型1、类型2、类型3”，其他脸型请自测。
    2. 现在阶段仅支持女性角色，男性角色自测。
    3. 现阶段AI并不能完美“复刻”人脸，仍需部分微调。
    4. 一般情况下，捏脸完成后需要微调一下，“眼”部分的“眼宽2”、“眼角Z轴”、“眼皮形状2”，“鼻子”部分视情况而定。
    
捐赠:
    欢迎访问下方链接进行捐赠支持，你的支持是我最大的动力，谢谢！
    捐赠1元: https://afdian.net/item/e197e2da17b711ee955252540025c377
    捐赠5元: https://afdian.net/item/38d47f9017b811eea1b55254001e7c00
    捐赠10元: https://afdian.net/item/5bde047017b811ee99085254001e7c00
-----------------------------------------------------------------------------------''')
            
        
        
    def openImage(self,):
        # QDialog(self).show()
        if not self.openBtn.isEnabled():
            return
        try:
            img_url,_=QFileDialog.getOpenFileUrl(self,"选择图片",QUrl(""),"Image(*.jpg;*.jpeg;*.png)")
            if img_url.url()=="":
                return
            self.img_path=img_url.url().split("///")[1]
            self.log(f"已选择图片: {self.img_path}\n")
        except:
            self.log(f"图片选择失败！\n")
            self.extractBtn.setDisabled(True)
            return
        
        self.extractBtn.setEnabled(True)
        # self.img_name = img_url.fileName().split(".")[0]
        # img_url=img_url.path()[1:]
        # img=cv2.imdecode(np.fromfile(img_path,dtype=np.uint8),-1)
        
    def process(self,):
        if self.img_path is None:
            self.log(f"请选择图片！\n")
        # self.log(f"正在提取，请稍等...\n")
        self.openBtn.setDisabled(True)
        img_path_splited = self.img_path.split(os.sep)
        img_name = img_path_splited[-1].split(".")[0]
        dir = os.sep.join(img_path_splited[:-1])
        self.save_path = os.path.join(dir,f"{img_name}.json")
        if not self.loadExtractor():
            return
            
        processor=Processor(self.extractor ,self.img_path,self.save_path)
        processor.done_signal.connect(self.process_done)
        processor.log_signal.connect(self.log)
        processor.finished.connect(lambda :processor.done_signal.disconnect())
        processor.start()
        
        
        
    def process_done(self,):
        self.extractBtn.setDisabled(True)
        self.openBtn.setEnabled(True)
        
        
    def log(self, message:str):
        self.LogBox.moveCursor(self.LogBox.textCursor().End)
        self.LogBox.append(message)
        
        
        
        

        




if __name__ =="__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app=QApplication(sys.argv)
    extractorWindow=ExtractorWindow()
    extractorWindow.show()
    sys.exit(app.exec())