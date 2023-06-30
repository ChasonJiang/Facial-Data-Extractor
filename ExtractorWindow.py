import os
import traceback
from Extractor import Extractor
from PyQt5.QtCore import QThread,pyqtSignal,QUrl
from PyQt5.QtWidgets import QWidget,QFileDialog,QDialog,QInputDialog
from ExtractorWindow_UI import Ui_Extractor 


class ExtractorWindow(QWidget,Ui_Extractor):
    def __init__(self, parent: QWidget | None=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        
        self.openBtn.clicked.connect(self.openImage)
        self.extractBtn.clicked.connect(self.process)
        self.img_path = None
        self.save_path = None
        # self.extractor=None
        self.hello()
    #     self.loadExtractor()
        
    # def loadExtractor(self,):
    #     try:
    #         self.extractor = Extractor()
    #     except:
    #         self.log("Extractor 加载失败！\n")
    #     self.log("Extractor 加载成功！\n")
        
    def hello(self,):
        self.log('''
\t欢迎使用 Facial Data Extractor


    本软件旨在利用AI从人物图像中提取人脸数据，用于辅助Illusion系列游戏中的人物捏脸。

    目前，只支持 AI Shoujo 和 Honey Select2。
    
作者：ChasonJiang
Github：https://github.com/ChasonJiang/Face-Data-Extractor

使用教程:
    Step1. 点击“打开图片”按钮, 选择图片。
    Step2. 点击“提取”按钮, 等待提取面部数据。
    Step3. 使用记事本或任意编辑器，打开提取完毕的json文件。

注意事项：
    1. 请保证待提取的人物图像五官清晰；不推荐人物面部尺寸与图像尺寸的比例小于四分之一（重要）
    2. 推荐提取3D风格的人物图像，真实世界的人物图像请自测。
    3. 现在阶段仅支持女性角色，男性角色自测。
---------------------------------------------------''')
            
        
        
    def openImage(self,):
        # QDialog(self).show()
        if not self.openBtn.isEnabled():
            return
        try:
            img_url,_=QFileDialog.getOpenFileUrl(self,"选择图片",QUrl(""),"Image(*.jpg;*.png)")
            self.img_path=img_url.url().split("///")[1]
            self.log(f"已选择图片: {self.img_path}\n")
        except:
            self.log(f"图片选择失败！\n")
            self.extractBtn.setDisabled(True)
        
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
        processor=Processor(self.img_path,self.save_path)
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
        
        
        
        
class Processor(QThread):
    done_signal = pyqtSignal()
    log_signal = pyqtSignal(str)
    def __init__(self, img_path:str,save_path:str):
        super().__init__()
        self.img_path = img_path
        self.save_path = save_path
        # self.extractor = extractor
        
    def run(self):
        extractor = None
        try:
            extractor = Extractor()
        except:
            self.log_signal.emit("Extractor 加载失败！\n")
            self.log_signal.emit(traceback.format_exc())
            self.done_signal.emit()
            return
            
        self.log_signal.emit("Extractor 加载成功！\n")
        self.log_signal.emit(f"正在提取，请稍等...\n")
        try:
            extractor.extract(self.img_path,self.save_path)
        except Exception as e:
            self.log_signal.emit(f"提取失败!\n") 
            self.log_signal.emit(traceback.format_exc())
            self.done_signal.emit()
            return 
        finally:
            del extractor
        self.log_signal.emit(f"提取成功! 面部数据文件已保存在 [{self.save_path}]\n")
        
        




if __name__ =="__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app=QApplication(sys.argv)
    extractorWindow=ExtractorWindow()
    extractorWindow.show()
    sys.exit(app.exec())