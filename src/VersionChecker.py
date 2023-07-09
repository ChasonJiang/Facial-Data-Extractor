from PyQt5.QtCore import QThread,pyqtSignal
import json
import requests

class VersionChecker(QThread):
    result_signal = pyqtSignal(dict)
    def run(self):
        headers={
            "Content-Type":"'text/html; charset=utf-8'"
        }
        url = "https://raw.githubusercontent.com/ChasonJiang/Facial-Data-Extractor/main/VersionInfo.json"
        try:
            res = requests.get(url,headers=headers,verify=False)
        except:
            self.result_signal.emit({"State":False,"msg":"请求失败，版本获取信息失败！\n"})
            return
        
        if res.status_code!=200:
            self.result_signal.emit({"State":False,"msg":"网络异常，版本获取信息失败！\n"})
            return
        versionInfo = json.loads(res.text)
        versionInfo["State"]=True
        self.result_signal.emit(versionInfo)
        

if __name__ =="__main__":

    headers={
        "Content-Type":"'text/html; charset=utf-8'"
    }
    url = "https://raw.githubusercontent.com/ChasonJiang/Facial-Data-Extractor/main/VersionInfo.json"
    res = requests.get(url,headers=headers,verify=False)
    print(res.json())