import requests
from bs4 import BeautifulSoup
import os   #操作檔案
from urllib import request  #純用cookie
from datetime import datetime

class smallFunction(object):

    @staticmethod
    def rearrange_files():
        path = 'storage/'
        num = 0
        for nowfolder in os.listdir(path):  #預設參數值為當前目錄
            for i, item in enumerate(os.listdir(path+nowfolder)):
                os.rename(path +nowfolder +'/'+item, path +nowfolder +'/' +str(i+1) +'.jpg')

