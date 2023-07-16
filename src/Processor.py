import traceback
from PyQt5.QtCore import QThread,pyqtSignal
from .Extractor import Extractor



class Processor(QThread):
    done_signal = pyqtSignal()
    log_signal = pyqtSignal(str)
    def __init__(self, extractor:Extractor, img_path:str,save_path:str):
        super().__init__()
        self.img_path = img_path
        self.save_path = save_path
        self.extractor = extractor
        
    def run(self):
        # extractor = None
        # try:
        #     extractor = Extractor()
        # except:
        #     self.log_signal.emit("Extractor 加载失败！\n")
        #     self.log_signal.emit(traceback.format_exc())
        #     self.done_signal.emit()
        #     return
            
        # self.log_signal.emit("Extractor 加载成功！\n")
        self.log_signal.emit(f"正在提取，请稍等...\n")
        try:
            self.extractor.extract(self.img_path,self.save_path, weight=[0.2,0.8])
        except Exception as e:
            self.log_signal.emit(f"提取失败!\n") 
            self.log_signal.emit(traceback.format_exc())
            self.done_signal.emit()
            return 
        # finally:
        #     del extractor
        self.log_signal.emit(f"提取成功! 面部数据文件已保存在 [{self.save_path}]\n")
        self.done_signal.emit()
        