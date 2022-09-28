from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from UI_main import Ui_MainWindow
from passwordDialog import PasswordForm
from smallFunction import smallFunction
import eynyCrawler
import os
import json
import time
# from fake_useragent import UserAgent

class MainController(QtWidgets.QMainWindow):
    def __init__(self):
        # in python3, super(Class, self).xxx = super().xxx
        super(MainController, self).__init__()  #呼叫一下自己出來
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self): #全域變數與初始化
        self.ui.buttonChooseConfirm.clicked.connect(self.choose_confirm)
        self.ui.buttonURLConfirm.clicked.connect(self.URL_confirm)
        self.ui.buttonReset.clicked.connect(self.initData)
        self.ui.buttonRename.clicked.connect(self.initData)
        self.initData()

        # 看降低什麼函數的頻率，或是使其定期觸發
        # timer = QTimer(self)
        # timer.timeout.connect(self.get_current_cursor_color)
        # timer.start(20)

    def initData(self):
        self.ui.textProcess.setText('程式已就緒')
        self.ui.labelCrawler.setText('')
        self.ui.inputURL.setText('')
        self.ui.comboChoose.setCurrentIndex(0)
        self.loginData = None
        self.newData = {}
        self.modeName = 'eyny'  #預設為eyny帳號

        #帳號密碼與cookie
        self.cookiecontent = {} #空dict給json
        try:
            with open("gitignore\cookie.json") as f:
                self.cookiecontent = json.load(f)
        except: pass
    
    def choose_confirm(self):
        self.ui.textProcess.append('已選擇 ' + self.ui.comboChoose.currentText())
        self.loginData = self.confirm_login_info(self.ui.comboChoose.currentIndex())

    def URL_confirm(self):
        if(self.loginData == None):
            self.ui.textProcess.append('請選擇爬蟲項目!') #之後改成msgbox
        else:
            self.crawler()

    #     self.qthread = ThreadTask()
    #     self.qthread.qthread_signal.connect(self.progress_changed)
    #     self.qthread.start_progress()
    
    # def progress_changed(self, value):        
    #     self.ui.textProcess.append(str(value))
    
    def confirm_login_info(self,mode):  #input 0:eyny圖片
        #output 0:無此key、 1:key值有問題、 2:正常 # 取值"User-Agent"、取值"Cookie"
        if(len(self.cookiecontent) == 0): return [0, None, None]
        else:
            if(mode == 0):
                self.modeName = 'eyny'
                if('eyny' in self.cookiecontent.keys()):
                    data = self.cookiecontent['eyny']
                    try: return [2, data['User-Agent'], data['Cookie']]  #之後要改
                    except: return [1, data, None]

    def crawler(self):
        if(self.loginData[0] != 2):
            if(self.loginData[0] == 0): self.dialog_password('無此網站登入資訊')
            if(self.loginData[0] == 1): self.dialog_password('登入資訊有問題，請重新輸入')

            if(self.newData['username'] != '') and (self.newData['password'] != ''): myun, mypw = self.newData['username'], self.newData['password']
            else:myUA, myCook = self.newData['User-Agent'], self.newData['Cookie']
            # elif(self.newData['User-Agent'] != '') and (self.newData['Cookie'] != ''): myUA, myCook = self.newData['User-Agent'], self.newData['Cookie']
            # else: self.dialog_password('輸入資訊有問題，請重新輸入')
        else:
            # myun, mypw = 
            myUA, myCook = self.loginData[1], self.loginData[2]
        #考量cookie過期
        # 理論上是2或是得到帳密cookie後，開始爬蟲
        temp = eynyCrawler.eynyphoto.photo_list(self.ui.inputURL.text(), myUA, myCook)
        self.ui.labelCrawler.setText(temp[1])
        self.ui.textProcess.append(temp[1] + '，圖片數量:' + str(len(temp[0])))
        eynyCrawler.eynyphoto.photo_crawler(temp[0], myUA, temp[1])
        self.ui.textProcess.append(temp[1] + ' 已下載完成')
    
    def dialog_password(self, contentStr):
        self.pwForm = QtWidgets.QWidget()
        self.pw = PasswordForm()
        self.pw.setupUi(self.pwForm)
        self.pw.labelcontent.setText(contentStr)
        self.pw.buttonconfirm_user.clicked.connect(self.dialog_password_confirm)
        self.pw.buttoncancel_user.clicked.connect(self.dialog_password_cancel)
        self.pwForm.show()

    def dialog_password_confirm(self):
        self.newData['username'] = self.pw.inputuser.text()
        self.newData['password'] = self.pw.inputpassword.text()
        self.newData['User-Agent'] = self.pw.inputUA.text()
        self.newData['Cookie'] = self.pw.inputcookie.text()
        self.dialog_password_dict()
        self.cookiecontent[self.modeName] = self.newData
        self.pwForm.close()

    def dialog_password_cancel(self):
        self.pwForm.close()
    
    def dialog_password_dict(self):
        if(self.newData['username'] == ''):
            try: self.newData['username'] = self.cookiecontent[self.modeName]['username']
            except: self.newData['username'] = ''
        if(self.newData['password'] == ''):
            try: self.newData['password'] = self.cookiecontent[self.modeName]['password']
            except: self.newData['password'] = ''
        if(self.newData['User-Agent'] == ''):
            try: self.newData['User-Agent'] = self.cookiecontent[self.modeName]['User-Agent']
            except: self.newData['User-Agent'] = ''
        if(self.newData['Cookie'] == ''):
            try: self.newData['Cookie'] = self.cookiecontent[self.modeName]['Cookie']
            except: self.newData['Cookie'] = ''

    def save_cookie(self):
        with open("gitignore\cookie.json", "w") as f: #存取資訊以方便下次使用
            json.dump(self.cookiecontent, f, indent = 4)
    
    def closeEvent(self, event):  #關閉視窗的事件
        self.save_cookie()
        print('window close')

class ThreadTask(QThread):  # 有點奇怪，沒有真的開到thread
    qthread_signal = pyqtSignal(int)

    def start_progress(self):
        max_value = 10
        for i in range(max_value):
            time.sleep(0.1)
            self.qthread_signal.emit(i+1)
            # self.ui.textProcess.append(i)
