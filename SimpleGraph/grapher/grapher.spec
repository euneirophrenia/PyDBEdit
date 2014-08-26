# -*- mode: python -*-
a = Analysis(['/Users/marcodivincenzo/Documents/Programmi/Python/SimpleGraph/main.py'],
             pathex=['/Users/marcodivincenzo/Downloads/python/PyInstaller-2.1/grapher'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='grapher',
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='grapher')
app = BUNDLE(coll,
             name='grapher.app',
             icon=None)
