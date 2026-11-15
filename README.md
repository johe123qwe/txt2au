# text2audio

微软服务器文本转到语音

## Installation

```
pip install -r requirements.txt
```

```
python app.py
```

## Packaged into pyqt software

```
pyinstaller build.spec
```

## Windows 打包

需要 Python、[7-Zip](https://www.7-zip.org/)、[Inno Setup 6](https://jrsoftware.org/isinfo.php)（`winget install 7zip.7zip JRSoftware.InnoSetup`）。

```
build_windows.bat                                  # 便携版 + 安装版
powershell -ExecutionPolicy Bypass -File build_windows.ps1 -Target portable    # 只打便携版
powershell -ExecutionPolicy Bypass -File build_windows.ps1 -Target installer   # 只打安装版
```

产物在 `dist\release\`，均为 7z 加密（默认密码 `123`，可用 `-Password` 修改）。

## GitHub 自动发布

推送 `v*` 标签后，`.github/workflows/release.yml` 会自动打包 Windows（便携版 + 安装版）和 macOS（arm64 + Intel）并发布到 Releases：

```
git tag v1.2.2 && git push origin v1.2.2
```

## Thanks

[edge-tts](https://github.com/rany2/edge-tts)

## License

文字转音频 is licensed under [GPLv3](./LICENSE).


### 问题
Windows上部分系统无法运行

```py
# 1. 首先添加详细的日志输出来定位问题
import sys
import traceback

def main():
    try:
        # 你的主程序代码
        pass
    except Exception as e:
        # 将错误信息写入日志文件
        with open('error_log.txt', 'w') as f:
            f.write(f"Error: {str(e)}\n")
            f.write(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()
```