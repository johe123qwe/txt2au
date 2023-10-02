import asyncio

import edge_tts
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal


def read_file(file) -> str:
    with open(file, "r") as f:
        return f.read()


async def amain(TEXT, VOICE, OUTPUT_FILE, RATE) -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE, rate=RATE)
    await communicate.save(OUTPUT_FILE)


class AudioThread(QThread):
    '''生成音频'''
    audio = pyqtSignal(str)

    def textcontent(self, TEXT) -> str:
        return TEXT

    def output_file(self, OUTPUT_FILE) -> str:
        return OUTPUT_FILE
    
    def speed(self, RATE) -> str:
        return RATE
    
    def voicetype(self, VOICE) -> str:
        return VOICE

    def run(self) -> None:
        self.audio.emit('\n音频生成中, 请稍后...')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(amain(self.textcontent, self.voicetype, self.output_file, self.speed))
            # print('音频已生成 {}'.format(self.output_file))
            self.audio.emit('\n音频已生成 {}'.format(self.output_file))
        except Exception as e:
            self.audio.emit("生成失败{}".format(str(e)))
