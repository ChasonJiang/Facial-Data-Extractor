# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['Launcher.py'],
    pathex=[],
    binaries=[],
    datas=[("C:\\Users\\14404\\.virtualenvs\\Extractor-PieuWTZ6\\Lib\\site-packages\\onnxruntime\\capi","onnxruntime\\capi"), ("models\\resnet34_head_1_epoch_30_with_colorjitter.onnx","models")],
    hiddenimports=[],
    hookspath=[],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Facial Data Extractor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
