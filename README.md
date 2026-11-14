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