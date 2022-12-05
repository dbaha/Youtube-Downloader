from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
import pytube
from moviepy.editor import *
from threading import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(547, 441)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, 50, 431, 61))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TitleLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setObjectName("TitleLabel")
        self.verticalLayout.addWidget(self.TitleLabel, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 130, 441, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LinkLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.LinkLabel.setFont(font)
        self.LinkLabel.setObjectName("LinkLabel")
        self.horizontalLayout.addWidget(self.LinkLabel)
        self.YoutubeLinkLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.YoutubeLinkLineEdit.setObjectName("YoutubeLinkLineEdit")
        self.horizontalLayout.addWidget(self.YoutubeLinkLineEdit)
        self.DownloadButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.download())
        self.DownloadButton.setGeometry(QtCore.QRect(160, 220, 231, 71))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.DownloadButton.setFont(font)
        self.DownloadButton.setObjectName("DownloadButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(60, 370, 441, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Youtube mp3 Downloader"))
        self.TitleLabel.setText(_translate("MainWindow", "Youtube Mp3 Downloader"))
        self.LinkLabel.setText(_translate("MainWindow", "Youtube Link : "))
        self.DownloadButton.setText(_translate("MainWindow", "Download"))

    def Mp4toMp3(self,mp4,mp3):
          mp4_without_frames = AudioFileClip(mp4)     
          mp4_without_frames.write_audiofile(mp3)     
          mp4_without_frames.close() 
    global statmsg, progress
    def download(self):
        self.statusbar.showMessage("downloading")
        _link=self.YoutubeLinkLineEdit.text()
        print(_link)
        try:
            yt=pytube.YouTube(_link)
        except:
             print("connection error or video not found")
             alert=QtWidgets.QMessageBox(text="connection error or video not found")    
             alert.exec()
        else:
            Mp4Files=yt.streams.get_audio_only("mp4")
            SaveFolder=str(Path.home()/"Downloads")
            Mp4Files.download(SaveFolder)
            print("downloading")
            DefaultFilename=Mp4Files.default_filename
            NewFilename=DefaultFilename.replace('mp4','mp3')
            print("change file name")
            TempMp4=SaveFolder+"\\"+DefaultFilename
            TempMp3=SaveFolder+"\\"+NewFilename
            self.Mp4toMp3(TempMp4,TempMp3)
            print("convert")
            os.remove(TempMp4)
            alert=QtWidgets.QMessageBox(text=f"{NewFilename}: Downloaded, saved in download folder enjoy :? ")    
            alert.exec()
            print("done")
    def UpdateUI(self):
        print("abc")

    def run(self):
        t1=Thread(target=self.download())
        t2=Thread(target=self.UpdateUI())
        t1.start
        t2.start


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
