# Window

# import modules
from PyQt5 import QtWidgets,QtGui
import sys
import demo1
import pyqtgraph as pg

class Window(demo1.Ui_Security, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        #set backgrounds
        pg.setConfigOptions(leftButtonPan=True)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

    def display_img(self, name, pos):
        img = QtGui.QPixmap("./Figs/"+name+".png")
        pos.setPixmap(img)

    def display_text(self, text, pos):
        pos.setText("{:3f}".format(text))
        #pos.setText("1")


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
