# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['lab_parser_gui_fixed_save_dialog.py'],
    pathex=[],
    binaries=[('tesseract\\tesseract.exe', 'tesseract'), ('tesseract\\tessdata', 'tesseract\\tessdata'), ('poppler\\Library\\bin', 'poppler\\Library\\bin')],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='lab_parser_gui_fixed_save_dialog',
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
    icon=['morgana.ico'],
)
