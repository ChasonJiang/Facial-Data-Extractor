import traceback
from typing import List
from PyQt5.QtCore import QThread,pyqtSignal
from .OnnxExtractor import OnnxExtractor



class Processor(QThread):
    done_signal = pyqtSignal()
    log_signal = pyqtSignal(str)
    def __init__(self, extractor:OnnxExtractor, img_path:List[str],save_path:List[str]):
        super().__init__()
        self.img_path = img_path
        self.save_path = save_path
        self.extractor = extractor
        
    def run(self):
        self.log_signal.emit(f"正在提取，请稍等...\n")
        for idx, item in enumerate(self.img_path):
            if item is None:
               self.log_signal.emit(f"跳过第{idx+1}张图片，图片路径为空！\n")
               continue

            self.log_signal.emit(f"正在提取第{idx+1}张图片...\n")
            try:
                self.extractor.extract(item,self.save_path[idx])
            except Exception as e:
                self.log_signal.emit(f"第{idx+1}张图片提取失败!\n") 
                self.log_signal.emit(traceback.format_exc())
                self.done_signal.emit()
                continue

            self.log_signal.emit(f"第{idx+1}张图片提取成功! 面部数据文件已保存在 [{self.save_path[idx]}]\n")
        
        self.log_signal.emit(f"提取完成！\n")
        self.done_signal.emit()
            