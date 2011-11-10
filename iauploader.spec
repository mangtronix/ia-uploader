# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'), os.path.join(CONFIGDIR,'support/useUnicode.py'), 'iauploader.py'],
             pathex=['/Users/mang/src/iauploader'],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build/pyi.darwin/iauploader', 'iauploader'),
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT( exe,
               a.binaries - [('libiconv.2.dylib', '', '')],
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'iauploader'))
app = BUNDLE(coll,
             name=os.path.join('dist', 'iauploader.app'))
