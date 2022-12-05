import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtCore import QSize
from threading import *
import pytube 
from moviepy.editor import *
from pathlib import Path

class LoadingDialog(QDialog):
     process=""
     progress=100
     
     def __init__(self,_link):
          super().__init__()
          layout=QVBoxLayout()
          ProgressBar=QProgressBar()
          ProgressBar.setMinimum(0)
          ProgressBar.setMaximum(self.progress)
          layout.addWidget(ProgressBar)
          self.msglabel=QLabel()
          self.msglabel.text= self.process
          layout.addWidget(self.msglabel)
          self.setLayout(layout)
          self.DownloadAndConvert(_link)

     def PopUpNotif(self,msg):
          alert = QMessageBox()
          alert.setText(msg)
          alert.exec()
     def mp4_to_mp3(self,mp4, mp3):    
          mp4_without_frames = AudioFileClip(mp4)     
          mp4_without_frames.write_audiofile(mp3)     
          mp4_without_frames.close()  
     

     def DownloadAndConvert(self,link):
          if MainWindow.StartDownload==True:
               print("running") 
               print(f"link from download and convert {link}")
               self.DownloadPath=str(Path.home()/ "Downloads")
               savefolder=self.DownloadPath

               # self.progresspercnt=5
               # self.setWindowTitle("Progress :Setup"+str(self.progresspercnt)+"%")
               # self.msglabel.setText="getlink"
               try:
                    # self.ProgressBar.setValue(10)
                    yt = pytube.YouTube(link)
               except:
                    print("connection error or video not found") 
                    LoadingDialog.PopUpNotif(self,"connection error or video not found ")
               else:
                    
                    # self.process.setValue(30)
                    mp4_files=yt.streams.get_audio_only("mp4")  
                    parent_dir = savefolder
                    mp4_files.download(parent_dir)
                    # self.ProgressBar.setValue(48)
                    default_filename = mp4_files.default_filename
                    new_filename = default_filename.replace('mp4','mp3')
                    # self.ProgressBar.setValue(76)
                    mp4_path=parent_dir+"\\"+default_filename
                    mp3_path=parent_dir+"\\"+new_filename
                    LoadingDialog.mp4_to_mp3(self,mp4_path,mp3_path)
                    # self.ProgressBar.setValue(88)
                    os.remove(mp4_path)
                    # self.ProgressBar.setValue(99)
                    LoadingDialog.PopUpNotif(self,f"{new_filename}: Downloaded, saved in download folder enjoy ")
                    print('done')
class MainWindow(QMainWindow):
     StartDownload=False
     process=""
     progress=0
    
     def inputprint(self,link:str,savefolder:str):
          print(self.textbox.text())
          print(savefolder)
     def thread(self):
          _link=self.textbox.text()
          loading=LoadingDialog(_link)
          print(f"link from thread: {_link}")
          # t1=Thread(target=LoadingDialog.DownloadAndConvert(self,_link))
          # t1.start()
          t2=Thread(target=loading.exec)
          t2.start()
                         
     def  __init__(self):
          super(MainWindow,self).__init__()
          self.setWindowTitle("Youtube Mp3 Downloader")
          self.setFixedSize(500,300)

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





    
