from PyQt5 import QtWidgets
from mainController import MainController
import os

if __name__ == '__main__':
    # confirm the folder first  # file can build directly
    if not os.path.exists('gitignore'):os.mkdir('gitignore')
    # f= open("/gitignore/cookie.txt","x")
    # if os.path.isfile('/gitignore/cookie.txt'):os.mknod('/gitignore/cookie.txt')

    # perform main
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainController()
    window.show()
    sys.exit(app.exec_())
    #test for webhook