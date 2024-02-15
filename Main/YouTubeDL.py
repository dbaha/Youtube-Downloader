from PyQt5 import QtCore, QtGui, QtWidgets
from pytube import YouTube
from moviepy.editor import AudioFileClip, VideoFileClip
from pathlib import Path
import os
import requests
from threading import *
from mutagen import File
from mutagen.mp4 import MP4
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, APIC, error
from AddCover import AddAlbumCover


class Ui_MainWindow(QtWidgets.QMainWindow):
     # Signal   
    statmsg= QtCore.pyqtSignal(str)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(307, 223)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #add listeners
        self.DownloadButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.download())
        self.DownloadButton.setGeometry(QtCore.QRect(10, 170, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.DownloadButton.setFont(font)
        self.DownloadButton.setObjectName("DownloadButton")
        self.convertBox = QtWidgets.QGroupBox(self.centralwidget)
        self.convertBox.setGeometry(QtCore.QRect(0, 70, 281, 91))
        self.convertBox.setObjectName("convertBox")
        self.radioButtonWav = QtWidgets.QRadioButton(self.convertBox)
        self.radioButtonWav.setGeometry(QtCore.QRect(10, 40, 80, 16))
        self.radioButtonWav.setObjectName("radioButtonWav")
        self.radioButtonMp3 = QtWidgets.QRadioButton(self.convertBox)
        self.radioButtonMp3.setGeometry(QtCore.QRect(10, 60, 166, 16))
        self.radioButtonMp3.setObjectName("radioButtonMp3")
        self.radioButtonMp4 = QtWidgets.QRadioButton(self.convertBox)
        self.radioButtonMp4.setGeometry(QtCore.QRect(10, 20, 166, 16))
        self.radioButtonMp4.setObjectName("radioButtonMp4")
        self.radioButtonMp4.setChecked(True)
        self.ytlinksBox = QtWidgets.QGroupBox(self.centralwidget)
        self.ytlinksBox.setGeometry(QtCore.QRect(0, 10, 311, 51))
        self.ytlinksBox.setObjectName("ytlinksBox")
        self.YoutubeLinkLineEdit = QtWidgets.QLineEdit(self.ytlinksBox)
        self.YoutubeLinkLineEdit.setGeometry(QtCore.QRect(10, 20, 291, 20))
        self.YoutubeLinkLineEdit.setObjectName("YoutubeLinkLineEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.statmsg.connect(self.statusbar.showMessage)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "YouTube Downloader"))
        self.DownloadButton.setText(_translate("MainWindow", "Download"))
        self.convertBox.setTitle(_translate("MainWindow", "Conver to:"))
        self.radioButtonWav.setText(_translate("MainWindow", ".wav(Audio)"))
        self.radioButtonMp3.setText(_translate("MainWindow", ".mp3(Audio)"))
        self.radioButtonMp4.setText(_translate("MainWindow", ".mp4(Video)"))
        self.ytlinksBox.setTitle(_translate("MainWindow", "YouTube Link"))


    def ConvertAudioFile(self,video,convert):
          mp4_without_frames = AudioFileClip(video)     
          mp4_without_frames.write_audiofile(convert,write_logfile=False,verbose=False,logger=None)     
          mp4_without_frames.close() 
   
    
    def download(self):
        self.statmsg.emit("Starting")
        _link=self.YoutubeLinkLineEdit.text()
        print("Link: ", _link)
        try:
            self.statmsg.emit("Searching Youtube video")
            yt=YouTube(_link)
        except Exception as e:
             self.statmsg.emit("Failed")
             print("Error :",e)
             alert=QtWidgets.QMessageBox(text="Error :"+str(e))   
             alert.setWindowTitle("Failed to download") 
             alert.exec()
        else:
            self.statmsg.emit("Video found")
            SaveFolder=Path.home().joinpath("Downloads")
            self.statmsg.emit("Downloading")
            Singer=yt.author
            Title=yt.title
            Thumbnailurl=yt.thumbnail_url
            print(f"{yt.author},{yt.title}")
            # checking condition 
            if self.radioButtonMp4.isChecked():
                #mp4 video
                Mp4Files=yt.streams.get_highest_resolution()
                Mp4Files.download(SaveFolder)
                DefaultFilename=Mp4Files.default_filename
            if self.radioButtonWav.isChecked():
                # wav
                print("audio wav")
                Mp4Files=yt.streams.get_audio_only("mp4")
                Mp4Files.download(SaveFolder)
                DefaultFilename=Mp4Files.default_filename
                NewFilename=DefaultFilename.replace('mp4','wav')
            if self.radioButtonMp3.isChecked():
                # mp3
                Mp4Files=yt.streams.get_audio_only("mp4")
                Mp4Files.download(SaveFolder)
                DefaultFilename=Mp4Files.default_filename
                NewFilename=DefaultFilename.replace('mp4','mp3')
            print(DefaultFilename)    
            print("downloading") 
            self.statmsg.emit("Converting")
            print("change file name")
            if self.radioButtonMp4.isChecked():
                print("downlaod video mp4")
                convertvideofile = str(SaveFolder.joinpath(DefaultFilename))
                mp4=MP4(convertvideofile)
                mp4['\xa9nam'] = Title 
                mp4['\xa9ART'] = Singer
                mp4.save()
                self.statmsg.emit("Downloaded")
                alert=QtWidgets.QMessageBox(text=f"Save location:{convertvideofile}")
            elif self.radioButtonMp3.isChecked():
                print("downlaod audio")
                convertvideofile = str(SaveFolder.joinpath(DefaultFilename))
                convertaudiofile = str(SaveFolder.joinpath(NewFilename))
                self.ConvertAudioFile(convertvideofile,convertaudiofile)
                convertaudiofile= convertaudiofile.replace("\\","\\\\")
                print("convert")
                os.remove(convertvideofile)
                # MP3 METADATA EDIT HERE 

                #download album cover
                thumbnail_filename = 'thumbnail.jpg' 
                thumbnail_path= str(SaveFolder.joinpath(thumbnail_filename))
                response = requests.get(Thumbnailurl)
                with open(thumbnail_path, 'wb') as file:
                    file.write(response.content)
                print(f'Thumbnail downloaded and saved as {thumbnail_filename}')
                thumbnail_path= thumbnail_path.replace("\\","\\\\")
                mp3=AddAlbumCover(convertaudiofile)
                mp3.add_art(thumbnail_path)
                mp3.show_art()
            
                mp3 = ID3(convertaudiofile)
                mp3.add(TIT2(encoding=3, text=Title))  
                mp3.add(TPE1(encoding=3, text=Singer))  
                mp3.save()
                self.statmsg.emit("Downloaded")
                alert=QtWidgets.QMessageBox(text=f"Save location:Downloads\{convertaudiofile}") 
            elif self.radioButtonWav.isChecked():
                print("downlaod audio")
                convertvideofile = str(SaveFolder.joinpath(DefaultFilename))
                convertaudiofile = str(SaveFolder.joinpath(NewFilename))
                self.ConvertAudioFile(convertvideofile,convertaudiofile)
                print("convert")
                os.remove(convertvideofile)
                self.statmsg.emit("Downloaded")
                alert=QtWidgets.QMessageBox(text=f"Save location:Downloads\{convertaudiofile}")    
            alert.setWindowTitle("Success")
            alert.exec()
            self.statmsg.emit("Success")
            print("done")

    def run(self):
        print("kepencet")
        t1 = Thread(target=self.download)
        t1.start()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())