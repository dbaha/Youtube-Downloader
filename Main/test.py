from PyQt5 import QtCore, QtGui, QtWidgets
from pytube import YouTube
from moviepy.editor import AudioFileClip
from pathlib import Path
import os
from threading import *

class Ui_MainWindow(QtWidgets.QMainWindow):
     # Signal   
    statmsg= QtCore.pyqtSignal(str)
    progressVal= QtCore.pyqtSignal(int)
    
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
        self.DownloadButton.setGeometry(QtCore.QRect(150, 280, 231, 71))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.DownloadButton.setFont(font)
        self.DownloadButton.setObjectName("DownloadButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(60, 370, 441, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(190, 190, 170, 41))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setChecked(True)
        self.horizontalLayout_2.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_2.addWidget(self.radioButton_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        
        # connect signal
        self.statmsg.connect(self.statusbar.showMessage)
        self.progressVal.connect(self.progressBar.setValue)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Youtube mp3 Downloader"))
        self.TitleLabel.setText(_translate("MainWindow", "Youtube Mp3 Downloader"))
        self.LinkLabel.setText(_translate("MainWindow", "Youtube Link : "))
        self.DownloadButton.setText(_translate("MainWindow", "Download"))
        self.label.setText(_translate("MainWindow", "Convert to:"))
        self.radioButton.setText(_translate("MainWindow", ".wav"))
        self.radioButton_2.setText(_translate("MainWindow", ".mp3"))


    def ConvertAudioFile(self,video,convert):
          mp4_without_frames = AudioFileClip(video)     
          mp4_without_frames.write_audiofile(convert,write_logfile=False,verbose=False,logger=None)     
        #    mp4_without_frames.write_audiofile(mp3,write_logfile=False,verbose=true, logger=bar)     
          mp4_without_frames.close() 
   
    
    def download(self):
        self.statmsg.emit("Starting")
        self.progressVal.emit(5)
        _link=self.YoutubeLinkLineEdit.text()
        print(_link)
        try:
            self.statmsg.emit("Searching Youtube video")
            self.progressVal.emit(15)
            yt=YouTube(_link)
        except:
             self.statmsg.emit("Video not found")
             self.progressVal.emit(100)
             print("connection error or video not found")
             alert=QtWidgets.QMessageBox(text="Connection error or video not found.")   
             alert.setWindowTitle("We have trouble :( ") 
             alert.exec()
        else:
            self.statmsg.emit("Video found, Getting audio")
            self.progressVal.emit(26)
            Mp4Files=yt.streams.get_audio_only("mp4")
            SaveFolder=Path.home().joinpath("Downloads")
            self.statmsg.emit("Downloading")
            self.progressVal.emit(57)
            Mp4Files.download(SaveFolder)
            # checking condition 
            DefaultFilename=Mp4Files.default_filename
            if self.radioButton.isChecked():
                # wav
                NewFilename=DefaultFilename.replace('mp4','wav')
            if self.radioButton_2.isChecked():
                # mp3
                NewFilename=DefaultFilename.replace('mp4','mp3') 
            print("downloading") 
            self.statmsg.emit("Converting")
            self.progressVal.emit(76)
            print("change file name")
            convertvideofile = SaveFolder.joinpath(DefaultFilename)
            convertaudiofile = SaveFolder.joinpath(NewFilename)
            self.progressVal.emit(89)
            self.ConvertAudioFile(convertvideofile,convertaudiofile)
            print("convert")
            self.progressVal.emit(95)
            os.remove(convertvideofile)
            self.statmsg.emit("Downloaded")
            self.progressVal.emit(100)
            alert=QtWidgets.QMessageBox(text=f"{NewFilename}: Downloaded, saved in download folder enjoy <3 ")    
            alert.setWindowTitle("Yeahh :) ")
            alert.exec()
            print("done")

    def run(self):
        t1=Thread(target=self.download())
        t1.start



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())