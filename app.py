import sys
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QHBoxLayout, 
                             QVBoxLayout, QApplication,
                             QMessageBox, QWidget, QComboBox, QPlainTextEdit)
from PyQt5.QtGui import QIcon
import tools
import os
import time
import json

root_path = os.path.join(os.path.dirname(__file__))
class Text2audio(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        QApplication.instance().setWindowIcon(
            QIcon(os.path.join(root_path, 'src', 'logo.png')))
        self.CharacterBox = QComboBox()
        with open(os.path.join(root_path, 'src', 'audio_type.json'), "r", encoding="utf-8") as f:
            text = json.load(f)
        self.CharacterBox.addItems(text['types'])
        self.CharacterBox.setCurrentIndex(287)

        self.ChangeSpeed = QComboBox()
        self.ChangeSpeed.addItems(["减速-50%", "减速-40%", "减速-30%", "减速-20%", "减速-10%", "正常速度", "加速+10%", "加速+20%", "加速+30%", "加速+40%", "加速+50%"])
        self.ChangeSpeed.setCurrentIndex(5)

        GenerButton = QPushButton("生成音频")
        exitButton = QPushButton("退出")

        exitButton.clicked.connect(self.exit_app)
        GenerButton.clicked.connect(self.t2a)

        self.textEdit = QPlainTextEdit()
        vbox = QVBoxLayout()

        vbox.addWidget(self.textEdit)
        self.textEdit.setPlaceholderText("请输入要转换的文字")

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.CharacterBox)
        hbox.addWidget(self.ChangeSpeed)
        hbox.addWidget(GenerButton)
        hbox.addWidget(exitButton)
        vbox.addLayout(hbox)

        self.setGeometry(650, 300, 450, 350)
        self.setWindowTitle('文字转音频1.2')

    def read_textEdit(self):
        text = self.textEdit.toPlainText()
        if text.find('音频生成中, 请稍后...') != -1:
            text = text[:text.find('音频生成中, 请稍后...')]
            return text
        else:
            return text

    def select_voice(self):
        select_voice = self.CharacterBox.currentText()
        select_type = select_voice.rsplit('-', 1)[0]
        return select_type

    def output_file(self):
        download_dir = os.path.expanduser("~/Downloads")
        time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())
        output_file = os.path.join(download_dir, '{}.mp3'.format(time_now))
        return output_file

    def speed(self):
        if self.ChangeSpeed.currentText() == "正常速度":
            select_speed = "+0%"
        else:
            select_speed = self.ChangeSpeed.currentText().split("速", 1)[1]
        return select_speed

    def t2a(self):
        if self.textEdit.toPlainText() == "":
            QMessageBox.critical(self, "错误", "请输入要转换的文字")
            return
        else:
            self.text2audio = tools.AudioThread()
            self.text2audio.textcontent = self.read_textEdit()
            self.text2audio.output_file = self.output_file()
            self.text2audio.speed = self.speed()
            self.text2audio.voicetype = self.select_voice()
            self.text2audio.audio.connect(self.textEdit.appendPlainText)
            scrollbar = self.textEdit.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
            self.text2audio.start()

    def exit_app(self):
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Text2audio()
    ex.show()
    sys.exit(app.exec())