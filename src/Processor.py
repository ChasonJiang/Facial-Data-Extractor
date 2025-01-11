import os
import traceback
from typing import List
from PyQt5.QtCore import QThread,pyqtSignal
from .Extractor import Extractor



class Processor(QThread):
    done_signal = pyqtSignal()
    log_signal = pyqtSignal(str)
    def __init__(self, extractor:Extractor, img_path:List[str], template_chara_path:str=None):
        super().__init__()
        self.img_path = img_path
        self.template_chara_path = template_chara_path
        self.extractor = extractor
        
    def run(self):
        if_failed=False
        self.log_signal.emit(f"正在提取，请稍等...\n")
        for idx, item in enumerate(self.img_path):
            if item is None:
               self.log_signal.emit(f"跳过第{idx+1}张图片，图片路径为空！\n")
               continue

            self.log_signal.emit(f"正在提取第{idx+1}张图片...\n")
            try:
                item=item.replace("\\",os.sep)
                item=item.replace("/",os.sep)
                save_dir=os.sep.join(item.split(os.sep)[:-1])
                self.extractor.extract(item, save_dir, template_path=self.template_chara_path)
            except Exception as e:
                self.log_signal.emit(f"第{idx+1}张图片提取失败!\n") 
                self.log_signal.emit(traceback.format_exc())
                self.done_signal.emit()
                if_failed = True
                continue

            self.log_signal.emit(f"第{idx+1}张图片提取成功! 人物卡已保存在 [{save_dir}]\n")
            
        if if_failed:
            self.log_signal.emit(f"部分图片提取失败，请检查日志！\n")
        else:
            self.log_signal.emit(f"提取完成！\n")
        self.done_signal.emit()
            