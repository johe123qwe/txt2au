#!/bin/bash

# 安装 brew install create-dmg
# rm -rf build dist  && pyinstaller build.spec && bash creat_image.sh
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# brew install create-dmg
mkdir -p ./dist/dmg

rm -r ./dist/dmg/*
cp -r "dist/文字转音频.app" dist/dmg 
test -f "dist/文字转音频.dmg" && rm "dist/文字转音频.dmg"
create-dmg \
  --volname "文字转音频" \
  --volicon "./src/app.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "文字转音频.app" 175 120 \
  --hide-extension "文字转音频.app" \
  --app-drop-link 425 120 \
  "dist/文字转音频.dmg" \
  "dist/dmg/"