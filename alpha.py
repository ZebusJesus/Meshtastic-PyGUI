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
layout = [  [sg.Text('Welcome to the Meshtastic Python GUI!!')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Radio Information'), sg.Button('Help'), sg.Button('QR')],
            [sg.Text('Make sure to enclose message in " ", this allows for spaces in messages')],
            [sg.Button('Send Message'), sg.InputText(key='-MSGINPUT-')],
            [sg.Button('Set Channel'), sg.Text('SF'), sg.InputText(key='-SFINPUT-'), sg.Text('CR'), sg.InputText(key='-CRINPUT-'), sg.Text('BW'), sg.InputText(key='-BWINPUT-')],
            [sg.Button('Channel Setup')]]

layout_ChannelSettings = [[sg.Text('Channel Settings')],
                          [print(values['-SFINPUT-'])]]

# Create the Window
window = sg.Window('Meshtatstic-PyGUI', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Radio Information': #if user clicks Radio Information
        os.system("meshtastic --info >info.text && pause") # outout radio information to txt file
        break
    if event == 'Help':
        os.system("meshtastic -h  && pause")
        break
    if event == 'QR':
        os.system("meshtastic --qr >QR.png")
        break
    if event == 'Send Message': #if user clicks send message take input and send to radio
        os.system("meshtastic --sendtext "+ values['-MSGINPUT-'])
        break
    if event == 'Set Channel':
        os.system("echo meshtastic --setchan spread_factor "+values['-SFINPUT-']+" --setchan coding_rate "+values['-CRINPUT-']+" --setchan bandwidth "+values['-BWINPUT-']+" > testchanset.txt")
        break
    if event == 'Channel Setup':
        window = sg.Window('Meshtastic-PyGUI Channel Setup',layout_ChannelSettings)
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
                print( "hello world")
        window.close()
window.close()
