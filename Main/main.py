import os
import sys
from PyQt5.QtWidgets import QProgressBar,QDialog,QWidget,QVBoxLayout, QMainWindow, QLabel,QHBoxLayout, QLineEdit,QPushButton ,QMessageBox, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import QSize
from threading import *
import pytube 
from moviepy.editor import *
from pathlib import Path

class MainWindow(QMainWindow):
     StartDownload=False
     progresspercnt=0
     def mp4_to_mp3(mp4, mp3):    
          mp4_without_frames = AudioFileClip(mp4)     
          mp4_without_frames.write_audiofile(mp3)     
          mp4_without_frames.close()  
     def thread(self):
          self.setWindowTitle("Progress "+str(self.progresspercnt)+"%")
          self.PopUpNotif("Starting")
          t1=Thread(target=self.DownloadAndConvert)
          t1.start()

     def DownloadAndConvert(self):
          if MainWindow.StartDownload==True:
               link=self.textbox.text()
               savefolder=self.DownloadPath
               self.progresspercnt=5
               self.setWindowTitle("Progress :Setup"+str(self.progresspercnt)+"%")
               yt = pytube.YouTube(link)
               self.progresspercnt=30
               self.setWindowTitle("Progress :Downloading "+str(self.progresspercnt)+"%")
               mp4_files=yt.streams.get_audio_only("mp4")  
               vids= yt.streams.all()
               self.progresspercnt=43
               self.setWindowTitle("Progress :Downloading "+str(self.progresspercnt)+"%")
               parent_dir = savefolder
               mp4_files.download(parent_dir)
               default_filename = mp4_files.default_filename
               new_filename = default_filename.replace('mp4','mp3')
               mp4_path=parent_dir+"\\"+default_filename
               mp3_path=parent_dir+"\\"+new_filename
               self.mp4_to_mp3(mp4_path,mp3_path)
               self.progresspercnt=83
               self.setWindowTitle("Progress :Converting "+str(self.progresspercnt)+"%")
               os.remove(mp4_path)
               self.progresspercnt=100
               self.setWindowTitle("Progress :Finished "+str(self.progresspercnt)+"%")
               print('done')
               self.PopUpNotif("Success, enjoy :)!! ")
               self.setWindowTitle("Youtube Mp3 Downloader")
     def inputprint(self,link:str,savefolder:str):
          print(self.textbox.text())
          print(savefolder)
     def PopUpNotif(self,msg):
               alert = QMessageBox()
               alert.setText(msg)
               alert.exec()          
     def  __init__(self):
          super(MainWindow,self).__init__()
          self.setWindowTitle("Youtube Mp3 Downloader")
          self.setFixedSize(400,300)

          MainScene= QVBoxLayout()
          self.DownloadPath=str(Path.home()/ "Downloads")
          print (self.DownloadPath)
          # user input
          InputLinkLayout= QHBoxLayout()
          InsertLinkTxt="Yotube Link"
          InputLinkLayout.addWidget(QLabel(InsertLinkTxt))
          self.textbox=QLineEdit(self)
          self.textbox.resize(280,40)
          self.textbox.move(20,20)

          InputLinkLayout.addWidget(self.textbox)
          MainScene.addLayout(InputLinkLayout)
     
          # download btn
          DownloadBtnTxt="Download"
          DownloadBtn=QPushButton(DownloadBtnTxt)
          MainScene.addWidget(DownloadBtn)
          
          
          DownloadBtn.clicked.connect(self.thread)
          # DownloadBtn.clicked.connect(lambda msg : PopUpNotif("wow"))
          MainWindow.StartDownload=True

          widget=QWidget()
          widget.setLayout(MainScene)
          self.setCentralWidget(widget)
          


if __name__== "__main__":
     app =QApplication(sys.argv)
     app.processEvents()

     window=MainWindow()          
     window.show()
     app.exec()





    
