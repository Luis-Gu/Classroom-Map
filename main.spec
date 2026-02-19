# -*- mode: python ; coding: utf-8 -*-
# ============================================================
#  Classroom Map — PyInstaller Spec
#  Gerador de Mapa de Sala de Aula
# ============================================================
#
#  Build command:
#    pyinstaller main.spec
#
#  Output:
#    dist/ClassroomMap/ClassroomMap.exe
#
# ============================================================

import os
import sys
from PyInstaller.utils.hooks import collect_data_files

# ── Paths ──
ROOT = os.path.abspath(SPECPATH)
ICON_FILE = os.path.join(ROOT, 'icon', 'app.ico')

# ── Data Files ──
# Include icon assets and any other resources
datas = [
    (os.path.join(ROOT, 'icon'), 'icon'),
]

# Collect customtkinter data files (themes, assets)
datas += collect_data_files('customtkinter')

# ── Hidden Imports ──
hiddenimports = [
    'PIL',
    'PIL.Image',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    'PIL.ImageTk',
    'customtkinter',
    'fpdf',
    'tkinter',
]

# ── Analysis ──
a = Analysis(
    ['main.py'],
    pathex=[ROOT],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'notebook',
        'pytest',
    ],
    noarchive=False,
    optimize=1,
)

# ── PYZ Archive ──
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None,
)

# ── Executable ──
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MapaDeSala',
    icon=ICON_FILE if os.path.exists(ICON_FILE) else None,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,               # Windowed app, no terminal
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version_info=None,
    uac_admin=False,
)

# ── Collect into folder ──
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MapaDeSala',
)
