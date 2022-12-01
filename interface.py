from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from interface_sh import Ui_OtakuShop_main_window
import sys 

class Mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Mywindow, self).__init__()
        self.ui = Ui_OtakuShop_main_window()
        self.ui.setupUi(self)

def application():
    app = QApplication(sys.argv)
    window = Mywindow()
 
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__": 
    application()