import sys
import os
import time
import json
import logging

from PyQt5.QtWidgets import (QMainWindow, QPushButton, QHBoxLayout,
                             QVBoxLayout, QApplication, QMessageBox, QWidget,
                             QComboBox, QPlainTextEdit, QLineEdit, QLabel,
                             QFileDialog)
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon

import tools

APP_VERSION = '1.2.2'
DEFAULT_VOICE = 'zh-CN-YunjianNeural-男'

# 打包后资源在 sys._MEIPASS 下
root_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))


def setup_logging():
    # 日志写到用户目录，打包后的工作目录（/ 或 Program Files）通常不可写
    log_dir = os.path.join(os.path.expanduser('~'), '.txt2au')
    try:
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(filename=os.path.join(log_dir, 'app.log'),
                            level=logging.DEBUG, encoding='utf-8',
                            format='%(asctime)s - %(levelname)s - %(message)s')
    except OSError:
        logging.basicConfig(level=logging.DEBUG)


class Text2audio(QMainWindow):

    def __init__(self):
        super().__init__()
        self.settings = QSettings('txt2au', 'txt2au')
        self.worker = None
        self.initUI()

    def initUI(self):
        QApplication.instance().setWindowIcon(
            QIcon(os.path.join(root_path, 'src', 'logo.png')))

        # 声音
        self.CharacterBox = QComboBox()
        with open(os.path.join(root_path, 'src', 'audio_type.json'), "r", encoding="utf-8") as f:
            self.CharacterBox.addItems(json.load(f)['types'])
        idx = self.CharacterBox.findText(DEFAULT_VOICE)
        self.CharacterBox.setCurrentIndex(max(idx, 0))

        # 语速
        self.ChangeSpeed = QComboBox()
        self.ChangeSpeed.addItems(["减速-50%", "减速-40%", "减速-30%", "减速-20%", "减速-10%", "正常速度",
                                   "加速+10%", "加速+20%", "加速+30%", "加速+40%", "加速+50%"])
        self.ChangeSpeed.setCurrentIndex(5)

        self.textEdit = QPlainTextEdit()
        self.textEdit.setPlaceholderText("请输入要转换的文字")

        # 输出位置
        self.dirEdit = QLineEdit(self.settings.value(
            'output_dir', os.path.expanduser("~/Downloads")))
        browseButton = QPushButton("选择目录…")
        browseButton.clicked.connect(self.choose_dir)
        self.nameEdit = QLineEdit()
        self.nameEdit.setPlaceholderText("文件名（留空按时间命名）")

        dirBox = QHBoxLayout()
        dirBox.addWidget(QLabel("保存到:"))
        dirBox.addWidget(self.dirEdit, 1)
        dirBox.addWidget(browseButton)
        nameBox = QHBoxLayout()
        nameBox.addWidget(QLabel("文件名:"))
        nameBox.addWidget(self.nameEdit, 1)

        # 按钮
        self.generateButton = QPushButton("生成音频")
        exitButton = QPushButton("退出")
        self.generateButton.clicked.connect(self.t2a)
        exitButton.clicked.connect(self.close)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.CharacterBox)
        hbox.addWidget(self.ChangeSpeed)
        hbox.addWidget(self.generateButton)
        hbox.addWidget(exitButton)

        vbox = QVBoxLayout()
        vbox.addWidget(self.textEdit)
        vbox.addLayout(dirBox)
        vbox.addLayout(nameBox)
        vbox.addLayout(hbox)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        self.setGeometry(650, 300, 520, 400)
        self.setWindowTitle('文字转音频' + APP_VERSION)
        self.statusBar().showMessage("就绪")

    def choose_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择保存目录", self.dirEdit.text())
        if d:
            self.dirEdit.setText(d)

    def select_voice(self):
        return self.CharacterBox.currentText().rsplit('-', 1)[0]

    def speed(self):
        text = self.ChangeSpeed.currentText()
        return "+0%" if text == "正常速度" else text.split("速", 1)[1]

    def output_file(self):
        """返回输出文件路径；用户取消或无效时返回 None"""
        out_dir = os.path.expanduser(self.dirEdit.text().strip())
        if not out_dir:
            QMessageBox.critical(self, "错误", "请选择保存目录")
            return None
        try:
            os.makedirs(out_dir, exist_ok=True)
        except OSError as e:
            QMessageBox.critical(self, "错误", "无法创建目录 {}\n{}".format(out_dir, e))
            return None

        name = self.nameEdit.text().strip()
        if not name:
            name = time.strftime("%Y%m%d%H%M%S", time.localtime())
        if not name.lower().endswith('.mp3'):
            name += '.mp3'
        path = os.path.join(out_dir, name)

        if os.path.exists(path):
            ret = QMessageBox.question(self, "文件已存在", "{} 已存在，是否覆盖？".format(path))
            if ret != QMessageBox.Yes:
                return None
        self.settings.setValue('output_dir', out_dir)
        return path

    def t2a(self):
        if self.worker is not None and self.worker.isRunning():
            return
        text = self.textEdit.toPlainText()
        if not text.strip():
            QMessageBox.critical(self, "错误", "请输入要转换的文字")
            return
        path = self.output_file()
        if path is None:
            return

        logging.info("Generating %s", path)
        self.worker = tools.AudioThread(text, self.select_voice(), path, self.speed(), self)
        self.worker.succeeded.connect(self.on_succeeded)
        self.worker.failed.connect(self.on_failed)
        self.worker.finished.connect(lambda: self.generateButton.setEnabled(True))
        self.generateButton.setEnabled(False)
        self.statusBar().showMessage("音频生成中, 请稍后...")
        self.worker.start()

    def on_succeeded(self, path):
        logging.info("Audio saved: %s", path)
        self.statusBar().showMessage("音频已生成 {}".format(path))

    def on_failed(self, err):
        logging.error("Generation failed: %s", err)
        self.statusBar().showMessage("生成失败")
        QMessageBox.critical(self, "生成失败", err)

    def closeEvent(self, event):
        if self.worker is not None and self.worker.isRunning():
            ret = QMessageBox.question(self, "退出", "音频还在生成中，确定退出？")
            if ret != QMessageBox.Yes:
                event.ignore()
                return
            self.worker.wait(3000)
        event.accept()


if __name__ == '__main__':
    setup_logging()
    logging.info("Starting application")
    try:
        app = QApplication(sys.argv)
        ex = Text2audio()
        ex.show()
        sys.exit(app.exec())
    except Exception:
        logging.critical("Critical error in application execution", exc_info=True)
        raise
