# ----- <About> ----- #
#   Author: Zebus Zebus
#   Email: zebusjesus@pm.me
#   Date: 3-13-21
#   Meshtastic PyGUI
#
import PySimpleGUI as sg

# ------ <Menu_Definition> ------ #

menu_def = [['&File', ['&Properties', 'E&xit']],
            ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Toolbar', ['---', 'Firmware Window', 'Radio Window',
                          '---', 'Command &3', 'Command &4']],
            ['&Help', '&About...'], ]

# ----- </Menu Definition> ----- #

def make_win1API():
    sg.theme('DarkAmber')
    sg.set_options(element_padding=(0, 0))


    layout = [
              [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
              [sg.Text('Welcome to the Meshtastic Python GUI!!  WARNING I AM NOT RESPONSIBLE FOR ERRORS OR BROKEN DEVICES, LOOK BEFORE YOUR RUN')],
              [sg.Button('Radio Information'), sg.Button('Help'), sg.Button('QR')],
              [sg.Button('Set Channel Settings'), sg.Text('SF'), sg.InputText(size=(10,1),key='-SFINPUT-'), sg.Text('CR'), sg.InputText(size=(10,1),key='-CRINPUT-'),
              sg.Text('BW'), sg.InputText(size=(10,1),key='-BWINPUT-')],
              [sg.Button('Set Long Slow'),sg.Button('Set Short Fast')],
              [sg.Button('Set URL'), sg.InputText(key='-URLINPUT-')],
              [sg.Button('Set Wifi SSID'),sg.Text('Wifi SSID'),sg.InputText(size=(20,1),key='-WifiSSID-'),sg.Button('Set Wifi Password'),sg.Text('Wifi Password'),sg.InputText(size=(20,1),key='-WifiPASS-')],
              [sg.Button("AP On"),sg.Button('AP Off')],
              [sg.Button('Set Owner'), sg.InputText(key='-OWNERINPUT-')],
              [sg.Button('Set Lattitude'),sg.InputText(size=(10,1),key='-SETLAT-'), sg.Button('Set Longitude'), sg.InputText(size=(10,1),key='-SETLON-'),
              sg.Button('Set Altitude'), sg.InputText(size=(10,1),key='-SETALT-')],
              [sg.Button('Set Router'), sg.Button('Unset Router')],
              [sg.Button('Firmware Window'), sg.Button('Radio Window')],
              [sg.Button('Close')]
             ]
    return sg.Window('Meshtastic API', layout, finalize=True, no_titlebar=True, grab_anywhere=True)

def make_win2FIRMWARE():  ##define Frimware Window loayout and conents
    layout = [
               [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
               [sg.Text('Hardware and  Firmware build selection')],
               [sg.Checkbox('T-Beam',key='-T-Beam-',enable_events=True),sg.Checkbox('heltec',key='-heltec-'),
                sg.Checkbox('T-LoRa',key='-T-LoRa-'),sg.Checkbox('LoRa Relay',key='-LoRa Relay-')],
               #[sg.Checkbox('ANZ',key='-ANZ-'),sg.Checkbox('CN',key='-CN-'),sg.Checkbox('EU865',key='-EU865-'),sg.Checkbox('EU443',key='-EU443-'),sg.Checkbox('JP',key='-JP-'),sg.Checkbox('KR',key='-KR-'),sg.Checkbox('US',key='-US-')],
               [sg.Checkbox('1.2.9',key='-1.2.9-'), sg.Checkbox('1.2.6',key='-1.2.6-'), sg.Checkbox('1.1.50',key='-1.1.50-'), sg.Checkbox('Hamster Nightly',key='-HN-')],
               [sg.Button('Download Firmware')],
               [sg.Input(key='_FILES_'), sg.FilesBrowse()],
               [sg.Text('The download just downloads the binary to a firmware.zip file in the local folder')],
               [sg.Text('and is extracted to a folder called firmware.')],
               [sg.Text('You can then browse to the needed binary in the firmware folder.')],
               [sg.Button('Flash Firmware'), sg.Button('Update Firmware'), sg.Cancel()],
               [sg.Button('Close')]
              ]
    return sg.Window('Firmware Utility', layout, finalize=True, no_titlebar=True, grab_anywhere=True)

    # ----- Radio I/O Window ----- #

def make_win3():  ##define Radio Window Layout and contents
    layout = [
             [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
             [sg.Text('Radio I/O')],
             [sg.Output(size=(80,25),key='-OUTPUT_RADIO-')],
             [sg.Button('Send Message'), sg.InputText(key='-MSGINPUT-')],
             [sg.Button('Send to node'),sg.Text('Messgage use " " if spaces are in message'),sg.InputText(size=(10,1),key='-NODE_MSG-'),
                sg.Text('Node'),sg.InputText(size=(10,1),key='-NODE-')],
             [sg.Button('Connect to Radio'), sg.Button('Close'),sg.Button('Close Radio Connection')]]
    return sg.Window('Radio I/O', layout, finalize=True, no_titlebar=True, grab_anywhere=True)

    # ----- /Radio I/O Window -----#
