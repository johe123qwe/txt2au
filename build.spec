# -*- mode: python ; coding: utf-8 -*-
import platform

block_cipher = None

if platform.system() == "Darwin":

    a = Analysis(['app.py'],
                pathex=[''],
                binaries=[],
                datas=[
                  ('./src', 'src/'),
                ],
                hiddenimports=['PyQt5'],
                hookspath=['hook'],
                runtime_hooks=[],
                excludes=[],
                win_no_prefer_redirects=False,
                win_private_assemblies=False,
                cipher=block_cipher,
                noarchive=False)
    pyz = PYZ(a.pure, a.zipped_data,
                cipher=block_cipher)
    exe = EXE(pyz,
              a.scripts,
              [],
              exclude_binaries=True,
              name='文字转音频',
              debug=False,
              bootloader_ignore_signals=False,
              strip=False,
              upx=True,
              console=False)
    coll = COLLECT(exe,
                  a.binaries,
                  a.zipfiles,
                  a.datas,
                  strip=False,
                  upx=True,
                  upx_exclude=[],
                  name='文字转音频')

    app = BUNDLE(
        coll,
        name='文字转音频.app',
        icon='./src/app.icns',
        bundle_identifier=None,
    )

elif platform.system() == "Windows":
    a = Analysis(
        ['app.py'],
        pathex=[],
        binaries=[],
        datas=[('./src', 'src/')],
        hiddenimports=[],
        hookspath=['hook'],
        hooksconfig={},
        runtime_hooks=[],
        excludes=[],
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=block_cipher,
        noarchive=False,
    )
    pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='文字转音频',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=['src\logo.ico'],
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='文字转音频',
    )