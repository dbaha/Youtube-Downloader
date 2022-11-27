from PyQt5.QtWidgets import QMessageBox, QLineEdit,QLabel,QApplication, QWidget, QPushButton, QVBoxLayout

# https://pythonspot.com/pyqt5-textbox-example/
# https://www.pythonguis.com/tutorials/pyqt-layouts/
app = QApplication([])
window=QWidget()
layout=QVBoxLayout()

textbox=QLineEdit()
textbox.resize(280,40)
textbox.move(20,20)
layout.addWidget(textbox)

button=QPushButton('download')
layout.addWidget(button)
def on_button_clicked():
    alert = QMessageBox()
    alert.setText('You clicked the button!')
    alert.exec()
button.clicked.connect(on_button_clicked)
window.setLayout(layout)
window.show()

app.exec()