# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['../run.py'],
    pathex=['..'],
    binaries=[],
    datas=[
        ('../app/ui/assets', 'app/ui/assets'), ('../assets', 'assets') 
    ],
    hiddenimports=[],
    hookspath=['./scripts/hooks'],  # This tells PyInstaller to use our correct hook
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
    a.zipfiles,
    a.datas,
    name='AnyText',
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
    icon='../assets/logo.ico'
)