
'''import PyInstaller.__main__
import os
PyInstaller.__main__.run([
#    'name-%s%' % 'dropletgame.exe',
     '--onefile',
     '--windowed',
     os.path.join('/home/rongke/coding/droplet/droplet', 'waterdrop.py')                                        

])
'''
import Tkinter

import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Droplet Game', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks Exit
        break
    print('You entered ', values[0])

window.close()
