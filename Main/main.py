import os
import sys
from PyQt5.QtWidgets import QWidget,QVBoxLayout, QMainWindow, QLabel,QHBoxLayout, QLineEdit,QPushButton ,QMessageBox, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import pytube 
from moviepy.editor import *
from pathlib import Path

class MainWindow(QMainWindow):

     StartDownload=False
     def mp4_to_mp3(mp4, mp3):    
          mp4_without_frames = AudioFileClip(mp4)     
          mp4_without_frames.write_audiofile(mp3)     
          mp4_without_frames.close() 
     def PopUpnotif(msg):
          alert = QMessageBox()
          alert.setText(msg)
          alert.exec()
     
     def downloadvideo(link,savefolder:str):
          if MainWindow.StartDownload==True:
               yt = pytube.YouTube(link)
               mp4_files=yt.streams.get_audio_only("mp4")  
               vids= yt.streams.all()
               parent_dir = savefolder
               mp4_files.download(parent_dir)
               default_filename = mp4_files.default_filename
               new_filename = default_filename.replace('mp4','mp3')
               mp4_path=parent_dir+"\\"+default_filename
               mp3_path=parent_dir+"\\"+new_filename
               MainWindow.mp4_to_mp3(mp4_path,mp3_path)
               os.remove(mp4_path)
               print('done')
               MainWindow.PopUpnotif("Success, enjoy :)!! ")

     def  __init__(self):
          super(MainWindow,self).__init__()
          self.setWindowTitle("Youtube Mp3 Downloader")
          MainScene= QVBoxLayout()
          DownloadPath=str(Path.home()/ "Downloads")
          print (DownloadPath)
          # user input
          InputLinkLayout= QHBoxLayout()
          InsertLinkTxt="Yotube Link"
          InputLinkLayout.addWidget(QLabel(InsertLinkTxt))
          textbox=QLineEdit()
          textbox.resize(280,40)
          textbox.move(20,20)
          InputLinkLayout.addWidget(textbox)
          Link=textbox.text()
          # download btn
          DownloadBtnTxt="Download"
          DownloadBtn=QPushButton(DownloadBtnTxt)
          DownloadBtn.clicked.connect(MainWindow.downloadvideo(Link,str(DownloadPath)))
          MainWindow.StartDownload=True

          MainScene.addLayout(InputLinkLayout)
          MainScene.addWidget(DownloadBtn)
          
          widget=QWidget()
          widget.setLayout(MainScene)
          self.setCentralWidget(widget)
          
     

app =QApplication(sys.argv)
window=MainWindow()          
window.show()
app.exec()





    
