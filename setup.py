
import PyInstaller.__main__
import os
PyInstaller.__main__.run([
#    'name-%s%' % 'dropletgame.exe',
     '--onefile',
     '--windowed',
     os.path.join('/home/rongke/coding/droplet/droplet', 'waterdrop.py'),                                         

])