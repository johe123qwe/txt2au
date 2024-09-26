import sys
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QHBoxLayout, 
                             QVBoxLayout, QApplication,
                             QMessageBox, QWidget, QComboBox, QPlainTextEdit)
from PyQt5.QtGui import QIcon
import tools
import os
import time
import json
import logging

# 设置日志输出到文件
logging.basicConfig(filename='app.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.debug("Application started")

root_path = os.path.join(os.path.dirname(__file__))

class Text2audio(QMainWindow):

    def __init__(self):
        super().__init__()
        logging.info("Initializing Text2audio window")
        try:
            self.initUI()
        except Exception as e:
            logging.error("Error initializing UI", exc_info=True)

    def initUI(self):
        logging.info("Setting up UI components")
        try:
            QApplication.instance().setWindowIcon(
                QIcon(os.path.join(root_path, 'src', 'logo.png')))
            self.CharacterBox = QComboBox()

            # 读取音频类型配置文件
            with open(os.path.join(root_path, 'src', 'audio_type.json'), "r", encoding="utf-8") as f:
                text = json.load(f)
            self.CharacterBox.addItems(text['types'])
            self.CharacterBox.setCurrentIndex(287)

            # 设置语速选项
            self.ChangeSpeed = QComboBox()
            self.ChangeSpeed.addItems(["减速-50%", "减速-40%", "减速-30%", "减速-20%", "减速-10%", "正常速度", "加速+10%", "加速+20%", "加速+30%", "加速+40%", "加速+50%"])
            self.ChangeSpeed.setCurrentIndex(5)

            # 创建按钮
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
            logging.info("UI components successfully set up")

        except Exception as e:
            logging.error("Error during UI setup", exc_info=True)

    def read_textEdit(self):
        try:
            text = self.textEdit.toPlainText()
            if '音频生成中, 请稍后...' in text:
                text = text[:text.find('音频生成中, 请稍后...')]
                logging.debug("Processed text from textEdit: %s", text)
            return text
        except Exception as e:
            logging.error("Error reading text from textEdit", exc_info=True)

    def select_voice(self):
        try:
            select_voice = self.CharacterBox.currentText()
            select_type = select_voice.rsplit('-', 1)[0]
            logging.debug("Selected voice type: %s", select_type)
            return select_type
        except Exception as e:
            logging.error("Error selecting voice type", exc_info=True)

    def output_file(self):
        try:
            download_dir = os.path.expanduser("~/Downloads")
            time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())
            output_file = os.path.join(download_dir, '{}.mp3'.format(time_now))
            logging.debug("Output file path: %s", output_file)
            return output_file
        except Exception as e:
            logging.error("Error generating output file path", exc_info=True)

    def speed(self):
        try:
            if self.ChangeSpeed.currentText() == "正常速度":
                select_speed = "+0%"
            else:
                select_speed = self.ChangeSpeed.currentText().split("速", 1)[1]
            logging.debug("Selected speed: %s", select_speed)
            return select_speed
        except Exception as e:
            logging.error("Error selecting speed", exc_info=True)

    def t2a(self):
        logging.info("Generate audio button clicked")
        try:
            if self.textEdit.toPlainText() == "":
                logging.warning("No text input found")
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
                logging.info("Audio generation thread started")
        except Exception as e:
            logging.error("Error in t2a (text to audio) method", exc_info=True)

    def exit_app(self):
        logging.info("Exit button clicked, closing application")
        sys.exit()

if __name__ == '__main__':
    try:
        logging.info("Starting application")
        app = QApplication(sys.argv)
        ex = Text2audio()
        ex.show()
        sys.exit(app.exec())
    except Exception as e:
        logging.critical("Critical error in application execution", exc_info=True)
