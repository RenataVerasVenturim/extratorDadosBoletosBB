# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('static/style.css', 'static'), ('static/script.js', 'static'), ('static/imgp.jpg', 'static'), ('static/imgg.jpg', 'static'), ('static/logo.png', 'static'), ('static/faviconuff.ico', 'static'), ('static/icon.jpg', 'static'), ('templates/index.html', 'templates'), ('pdfs/Seu boleto 1.pdf', 'pdfs'), ('pdfs/Seu boleto 2.pdf', 'pdfs'), ('pdfs/Sua nota de empenho.pdf', 'pdfs'), ('pdfs/Temp_Consolidado.xlsx', 'pdfs'), ('Modelo.xlsx', '.'), ('ModeloParaAjustesNosCampos.xltm', '.'), ('README.md', '.'), ('requirements.txt', '.'), ('LICENSE', '.'), ('RascunhosGerados/Rascunho-32.xlsx', 'RascunhosGerados')],
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
    name='app',
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
    icon=['static\\IconeApp.ico'],
)
