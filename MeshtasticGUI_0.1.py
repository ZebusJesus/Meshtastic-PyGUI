#Zebus   zebusjesus@pm.me       I AM NOT A PROGRAMER PLEASE BE GENTAL!!!!
#
#The goal of this project it to provide a simple GUI that uses the Mestashtic API for interacting with radios
#I am doing this because I want to create a tounch input for a project I am making and it will use the serial
#connection
#I did not create Meshtastic, this is only a GUI for the avialible API
#
#known issues:
# 1 - Text input requires "" in order to allow whitepaces in messages

import PySimpleGUI as sg
import os


sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Welcome to the Meshtastic Python GUI!!  WARNING I AM NOT RESPONSIBLE FOR ERRORS OR BROKEN DEVICES, LOOK BEFORE YOUR RUN')],
            [sg.Button('Radio Information'), sg.Button('Help'), sg.Button('QR')],
            [sg.Text('Make sure to enclose message in " ", this allows for spaces in messages')],
            [sg.Button('Send Message'), sg.InputText(key='-MSGINPUT-')],
            [sg.Button('Set Channel Settings'), sg.Text('SF'), sg.InputText(size=(10,1),key='-SFINPUT-'), sg.Text('CR'), sg.InputText(size=(10,1),key='-CRINPUT-'),
                sg.Text('BW'), sg.InputText(size=(10,1),key='-BWINPUT-')],
            [sg.Button('Set Long Slow'),sg.Button('Set Short Fast')],
            [sg.Button('Set URL'), sg.InputText(key='-URLINPUT-')],
            [sg.Button('Set Owner'), sg.InputText(key='-OWNERINPUT-')],
            [sg.Button('Set Lattitude'),sg.InputText(size=(10,1),key='-SETLAT-'), sg.Button('Set Longitude'), sg.InputText(size=(10,1),key='-SETLON-'),
                sg.Button('Set Altitude'), sg.InputText(size=(10,1),key='-SETALT-')],
            [sg.Button('Set Router'), sg.Button('Unset Router')],
            [sg.Text('In order to use the flash tool your environmental variables must be configured')],
            [sg.Text('Python, Git for Windows, and esptools must be installed and configured')],
            [sg.Text('If you have installed Visual Studio with Python Support your path will not be standard and will be located where you installed visual studio')],
            [sg.Input(key='_FILES_'), sg.FilesBrowse()],
            [sg.Button('Flash Firmware'), sg.Button('Update Firmware'), sg.Cancel()]

        ]
# Create the Window
window = sg.Window('Meshtatstic-PyGUI', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        window.close()
        break
    if event == 'Radio Information': #if user clicks Radio Information

        os.system("meshtastic --info >radioinfo.txt") # outout radio information to txt file
    if event == 'Help':
        os.system("meshtastic -h")
    if event == 'QR':
        os.system("meshtastic --qr >QR.png")
    if event == 'Send Message': #if user clicks send message take input and send to radio
        os.system("meshtastic --sendtext "+ values['-MSGINPUT-'])
    if event == 'Set Channel':
        os.system("echo meshtastic --setchan spread_factor "+values['-SFINPUT-']+" --setchan coding_rate "+values['-CRINPUT-']+" --setchan bandwidth "+values['-BWINPUT-']+" >>log.txt")
    if event == 'Set URL':
        os.system("meshtatic --seturl "+values['-URLINPUT-'])
    if event == 'Set Long Slow':
        os.system("meshtastic --setch-longslow")
    if event == 'Set Short Fast':
        os.system("meshtastic --setch-shortfast")
    if event == 'Set Owner':
        os.system("meshtastic --setowner "+values['-OWNERINPUT-'])
    if event == 'Set Lattitude':
        os.system("meshtastic --setlat "+values['-SETLAT-'])
    if event == 'Set Longitude':
        os.system("meshtastic --setlon "+values['-SETLON-'])
    if event == 'Set Altitude':
        os.system("meshtastic --setalt "+values['-SETALT-'])
    if event == 'Set Router':
        os.system("echo meshtastic --setrouter")
    if event == 'Unset Router':
        os.system("echo meshtastic --unset-router")
    if event == "Flash Firmware": # this command requires .sh files be able to be handled by the system, windows can us
        os.system("sh device-install.sh -f "+values['_FILES_'])
    if event == "Update Firmware":# update firmware while keeping settings in place
        os.system("sh device-update.sh -f "+values['_FILES_'])
