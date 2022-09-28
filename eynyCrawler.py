import requests
from bs4 import BeautifulSoup
import os   #操作檔案
from urllib import request  #純用cookie
from datetime import datetime

class eynyphoto(object):

    @staticmethod
    def photo_title(rowstring): #將文章名稱的特殊字元直接用在資料夾名稱可能有問題 #[我的腦內戀礙選項] [15P] 人物圖
        rowstring = rowstring.replace(" ","")
        items = rowstring.split("]")
        for item in items:
            if "P圖" not in item:
                return item[1:]
        return "the title error! photo_title"

    @staticmethod
    def photo_list(URL, userStr, cookieStr):
        URL_headers = {
            "User-Agent": userStr,
            "Cookie": cookieStr
        }
        with requests.Session() as s:
            target = s.get(URL, headers=URL_headers)  #目標位置
            soup = BeautifulSoup(target.text, "html.parser")

            rowData = soup.find_all('ignore_js_op')  #圖片位置
            filterData = list(map(lambda x: x.find('img').get('file'), rowData))
        
        #文章名稱&資料夾名稱
        folderTitle = eynyphoto.photo_title(soup.find(id='thread_subject').string)
        if not os.path.exists('storage'): os.mkdir('storage')
        if not os.path.exists('storage/'+folderTitle): os.mkdir('storage/'+folderTitle)
        
        return [filterData, folderTitle]
    
    @staticmethod
    def photo_crawler(photoDataList, userStr, title):
        photo_headers = {
            'User-Agent': userStr,
        }
        file_title = datetime.now().strftime('%m%d-%H%M%S_') #現在時間
            
        for index,link in enumerate(photoDataList):
            img = requests.get(link, headers=photo_headers)  # 圖片網址
            # imgSize = img.size() #因為非檔案而是request

            with open('storage/' + title +"\\" + file_title +str(index+1) + ".jpg", "wb") as file:  # 開啟資料夾及命名圖片檔
                file.write(img.content)  # 寫入圖片的二進位碼
