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


# ---------------- 检查更新 ----------------
import json
import re
import ssl
import urllib.error
import urllib.request

GITHUB_REPO = 'johe123qwe/txt2au'
LATEST_RELEASE_API = 'https://api.github.com/repos/{}/releases/latest'.format(GITHUB_REPO)
RELEASES_PAGE = 'https://github.com/{}/releases'.format(GITHUB_REPO)


def parse_version(v):
    """'v1.2.10' -> (1, 2, 10)，用于比较大小"""
    return tuple(int(n) for n in re.findall(r'\d+', v or ''))


def is_newer(latest, current):
    return parse_version(latest) > parse_version(current)


def _ssl_context():
    # 打包后的 Python 可能找不到系统证书，优先使用 certifi（edge-tts 的依赖）
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


def fetch_latest_release(timeout=10):
    """返回 GitHub 最新发布 {'version', 'url', 'notes'}；尚无发布时返回 None"""
    req = urllib.request.Request(LATEST_RELEASE_API, headers={
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'txt2au-update-checker',
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_context()) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    return {
        'version': data.get('tag_name', '').lstrip('vV'),
        'url': data.get('html_url') or RELEASES_PAGE,
        'notes': data.get('body') or '',
    }


class UpdateCheckThread(QThread):
    '''后台检查更新，避免网络请求卡住界面'''
    succeeded = pyqtSignal(object)  # dict 或 None
    failed = pyqtSignal(str)

    def run(self) -> None:
        try:
            self.succeeded.emit(fetch_latest_release())
        except Exception as e:
            self.failed.emit(str(e))
