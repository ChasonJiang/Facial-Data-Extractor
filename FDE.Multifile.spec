# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['Launcher.py'],
    pathex=[],
    binaries=[],
    datas=[("C:\\Users\\14404\\Project\\FDE\\.conda\\Lib\\site-packages\\onnxruntime\\capi","onnxruntime\\capi"), 
            ("src\\weights\\model.onnx","src\\weights\\"),
            ("src\\face_data_utils\\MsgToJson","src\\face_data_utils\\MsgToJson"),
            ("src\\face_data_utils\\parameter_flags.json","src\\face_data_utils\\"),
            ("src\\face_data_utils\\statistical_bone_data.json","src\\face_data_utils\\"),
            ("src\\face_data_utils\\statistical_face_data.json","src\\face_data_utils\\"),
            ("src\\assets","src\\assets"),
            ("src\\version","src"),
            ("C:\\Users\\14404\\Project\\FDE\\.conda\\Lib\\site-packages\\mtcnn_ort\\onet.onnx","mtcnn_ort"),
            ("C:\\Users\\14404\\Project\\FDE\\.conda\\Lib\\site-packages\\mtcnn_ort\\pnet.onnx","mtcnn_ort"),
            ("C:\\Users\\14404\\Project\\FDE\\.conda\\Lib\\site-packages\\mtcnn_ort\\rnet.onnx","mtcnn_ort")
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
    name='FDE',
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
    name='FDE',
)