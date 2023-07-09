# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['Launcher.py'],
    pathex=[],
    binaries=[],
    datas=[("C:\\Users\\14404\\.virtualenvs\\Extractor-PieuWTZ6\\Lib\\site-packages\\onnxruntime\\capi","onnxruntime\\capi"), 
            ("src\\models\\resnet50_face.onnx","src\\models"),
            ("src\\models\\resnet50_eyes.onnx","src\\models"),
            ("C:\\Users\\14404\\.virtualenvs\\Extractor-PieuWTZ6\\Lib\\site-packages\\\mtcnn_ort\\onet.onnx","mtcnn_ort"),
            ("C:\\Users\\14404\\.virtualenvs\\Extractor-PieuWTZ6\\Lib\\site-packages\\\mtcnn_ort\\pnet.onnx","mtcnn_ort"),
            ("C:\\Users\\14404\\.virtualenvs\\Extractor-PieuWTZ6\\Lib\\site-packages\\\mtcnn_ort\\rnet.onnx","mtcnn_ort")
            ],
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
    [],
    exclude_binaries=True,
    name='Facial Data Extractor',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Launcher',
)