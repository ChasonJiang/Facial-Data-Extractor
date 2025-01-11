import traceback
from PyQt5.QtCore import QThread,pyqtSignal
import json
import requests

class VersionChecker(QThread):
    result_signal = pyqtSignal(dict)
    def run(self):
        headers={
            "Content-Type":"'text/html; charset=utf-8'"
        }

        urls = [
            "http://43.136.47.104:14409/facial_data_extrator/update",
            "https://cdn.jsdelivr.net/gh/ChasonJiang/Facial-Data-Extractor@main/VersionInfo.json"
        ]

        for url in urls:
            try:
                res = requests.get(url,headers=headers,verify=False, timeout=5)
                if res.status_code == 200:
                    versionInfo = json.loads(res.text)
                    versionInfo["State"]=True
                    self.result_signal.emit(versionInfo)
                    return
                else:
                    continue
            except:
                continue

                
        self.result_signal.emit({"State":False,"msg":f"网络错误，版本检查失败！\n"})



if __name__ =="__main__":

    headers={
        "Content-Type":"'text/html; charset=utf-8'"
    }
    url = "http://106.52.148.60:14406/facial_data_extrator/update"
    res = requests.get(url,headers=headers,verify=False)
    print(json.loads(res.text))