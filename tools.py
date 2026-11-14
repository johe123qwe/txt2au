import asyncio

import edge_tts
from PyQt5.QtCore import QThread, pyqtSignal


async def amain(text, voice, output_file, rate) -> None:
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_file)


class AudioThread(QThread):
    '''生成音频'''
    succeeded = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(self, text, voice, output_file, rate, parent=None):
        super().__init__(parent)
        self.text = text
        self.voice = voice
        self.output_file = output_file
        self.rate = rate

    def run(self) -> None:
        try:
            asyncio.run(amain(self.text, self.voice, self.output_file, self.rate))
            self.succeeded.emit(self.output_file)
        except Exception as e:
            self.failed.emit(str(e))
