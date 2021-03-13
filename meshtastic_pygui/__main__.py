# ----- <About> ----- #
#   Author: Zebus Zebus
#   Email: zebusjesus@pm.me
#   Date: 3-13-21
#   Meshtastic PyGUI
#

# ----- <Imports> ----- #

import PySimpleGUI as sg
import os
import requests
import meshtastic
import subprocess
import time
from pubsub import pub
from zipfile import ZipFile
#from window_layout import make_win1API, make_win2FIRMWARE, make_win3

# ----- </IMports> ----- #

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
               [sg.Checkbox('1.2.10',key='-1.2.10-'), sg.Checkbox('1.2.6',key='-1.2.6-'), sg.Checkbox('1.1.50',key='-1.1.50-'), sg.Checkbox('Hamster Nightly',key='-HN-')],
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


# ----- Draw_Windows ----- #
def main():
    window1API, window2, window3 = make_win1API(), make_win2FIRMWARE(), make_win3()

    window2.move(window1API.current_location()[0]+220, window1API.current_location()[1]+220)

    window3.move(window1API.current_location()[0], window1API.current_location()[1]+420)
# ----- /Draw_Windows ----- #


# --- Start Script Loop checking for events ----- #
    while True:             # Event Loop
        window, event, values = sg.read_all_windows()

# ----- Close Windows and program ----- #
        if window == sg.WIN_CLOSED:     # if all windows were closed
            break
        elif event == 'Exit':
            break

        if event == sg.WIN_CLOSED or event == 'Close':
            window.close()
            if window == window2:       # if closing win 2, mark as closed
                window2 = None
            elif window == window1API:     # if closing win 1, mark as closed
                window1API = None
            elif window == window3:
                window3 = None
# ------ /Close Windows and programs ----- #

# ----- Menu About ----- #
        elif event == 'About...':
            window.disappear()
            sg.popup('About this program', 'Version 0.1.3',
                     'Meshtastic-PyGUI is a community based project,',
                     'More Info at https://www.meshtastic.org',
                     'Meshtastic version',meshtastic_version,
                     'PySimpleGUI Version', sg.version,  grab_anywhere=True)
            window.reappear()
# ----- /Menu About ----- #

# ----- Open ----- #


# ----- /Open ----- #

# ----- Properties ----- #
        elif event == 'Properties':
            try:
                os.system('meshtastic --info >radioinfo.txt')
                f = open('radioinfo.txt', 'r')
                file_contents = f.read()
                sg.popup(print(file_contents))
            except:
                output_window = window3
                sg.popup('No Device Present')
# ----- /Properties ----- #

        elif event == 'Close Radio Connection':

            #os.system("devcon.exe hwids * >>hwid.txt")
            try:
                output_window = window3
                meshtastic.SerialInterface().close(self)
            except:
                output_window = window3
                print('Error Closing Serial Connection')

# ----- Open Firmware Window ----- #
        elif event == 'Firmware Window':
            if not window2:
                window2 = make_win2FIRMWARE()
                window2.move(window1API.current_location()[0], window1API.current_location()[1] + 220)
# ----- /Open firmware Window ----- #

# ----- Open Radio I/O Window ----- #
        elif event == 'Radio Window':
            if not window3:
                window3 = make_win3()
                window3.move(window1API.current_location()[0], window1API.current_location()[1] - 220)
# ----- /Open Radio I/O Window ----- #

        elif event == '-IN-':
            # output_window = window3
            if output_window:           # if a valid window, then output to it
                output_window['-OUTPUT-'].update(values['-IN-'])
            else:
                window['-OUTPUT-'].update('Other window is closed')
# ----- Open COM connection to Radio ----- #
        elif event == 'Connect to Radio':
            try:
                output_window = window3
                interface = meshtastic.SerialInterface()
                def onReceive(packet, interface): # called when a packet arrives
                    print(f'Received: {packet}')

                def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
                    # defaults to broadcast, specify a destination ID if you wish
                    meshtastic.SerialInterface().sendText('hello mesh')

                print(pub.subscribe(onReceive, 'meshtastic.receive'))
                print(pub.subscribe(onConnection, 'meshtastic.connection.established'))
                # By default will try to find a meshtastic device, otherwise provide a device path like /dev/ttyUSB0
            except:
                output_window = window3
                print("Error connecting to radio")
# ---- /Open COM connection to Radio ----- #

# ----- Get Radio info ----- #
        elif event == 'Radio Information': #if user clicks Radio Information
            try:
                os.system('meshtastic --info >radioinfo.txt') # outout radio information to txt file
            except:
                output_window = window3
                print('Error getting radio info')
# ----- /Get Raadio info ---- #

# ----- Send Message ----- #
        elif event == 'Send Message': #if user clicks send message take input and send to radio
            try:
                os.system('meshtastic --sendtext '+ values['-MSGINPUT-'])
            except:
                output_window = window3
                print('Error sending message')
# ----- /Send Message ----- #

        elif event == 'Send Message to node':
            try:
                os.system('meshtastic --dest '+ values['-NODE-']+' --sendtext '+values['-NODE_MSG-'])
            except:
                output_window = window3
                print('Error sending message to '+values['-NODE-'])
# ----- Help ----- #
        elif event == 'Help':
            output_window = window3
             #if user clicks the help button
            os.system('meshtastic -h >help.txt')
            help_read = open('help.txt') #output meshtastic help via cmd prompt
            rh= help_read.read()
            print(rh)

# ----- QR ----- #
        elif event == 'QR':#if user clicks QR button
            try:
                os.system('meshtastic --qr >QR.tmp')
            except:
                output_window = window3
                os.system('echo ERROR QR >>error.log')
# ----- /QR ------ #

# ------ Set Channel -----#
        elif event == 'Set Channel': #if user clicks Set Channel button
            try:
                os.system('meshtastic --setchan spread_factor '+values['-SFINPUT-']+' --setchan coding_rate '+values['-CRINPUT-']+' --setchan bandwidth '+values['-BWINPUT-'])
            except:
                output_window = window3
                print('Error setting channel')
                os.system('echo ERROR Set Channel Event >>error.log')
# ------ /Set Channel ----- #

# ----- Set URL ----- #
        elif event == 'Set URL':
            try:
                os.system('meshtastic --seturl '+values['-URLINPUT-'])
            except:
                output_window = window3
                print('Error setting url')
                os.system('echo ERROR Set URL error >>error.log')
# ----- /Set URL ----- #

# ----- Set Long Slow ----- #
        elif event == 'Set Long Slow':
            try:
                os.system('meshtastic --setch-longslow')
            except:
                os.system('echo ERROR Set Channel LongSlow >>error.log')
# ------ /Set Long Slow ----- #

# ----- Set Short Fast ----- #
        elif event == 'Set Short Fast':
            try:
                os.system('meshtastic --setch-shortfast')
            except:
                os.system('echo ERROR Set Channel ShortFast >>error.log')
# ----- /Set Shor Fast ----- #

# ----- Set Owner ----- #
        elif event == 'Set Owner':
            os.system('meshtastic --setowner '+values['-OWNERINPUT-'])
# ----- /Set Owner ----- #

# ----- Set Lattitude -----#
        elif event == 'Set Lattitude':
            os.system('meshtastic --setlat '+values['-SETLAT-'])
# ----- /Set Lattitude ----- #

# ----- Set Longitude ----- #
        elif event == 'Set Longitude':
            os.system('meshtastic --setlon '+values['-SETLON-'])
# ----- /Set Longitude ----- #

# ----- Set Altitude ----- #
        elif event == 'Set Altitude':
            os.system('meshtastic --setalt '+values['-SETALT-'])
# -----/ Set Altitude ----- #

# ----- Set Router ----- #
        elif event == 'Set Router':
            os.system('meshtastic --set is_router true')
# ----- /Set Router ----- #

# ----- Unset Router ----- #
        elif event == 'Unset Router':
            os.system('echo meshtastic --set is_router false')
# ----- /Unset Router ----- #

# ----- Download Firmware ----- #
        elif event == 'Download Firmware':
            firmwareID = 'NULL'
            firmwarRegion = 'NULL'
            binVersion = 'NULL'
            try:
                # ----- Board Selection ----- #
                if values['-T-Beam-']:
                    firmwareID = '-tbeam'
                elif values['-heltec-']:
                    firmwareID = '-heltec'
                elif values['-T-LoRa-']:
                    firmwareID = '-tlora'
                elif values['-LoRa Relay-']:
                    firmwareID = '-lora-relay'
            except:
                print('firmwareid error')
                # ----- /Board Selection ----- #

            try:
                # ----- Region Selection ----- #
                if values['-ANZ-']:
                    firmwarRegion = '-ANZ'
                elif values['-CN-']:
                    firmwarRegion = '-CN'
                elif values['-JP-']:
                    firmwarRegion = '-JP'
                elif values['-KR-']:
                    firmwarRegion = '-KR'
                elif values['-EU443-']:
                    firmwarRegion = '-EU443'
                elif values['-EU865-']:
                    firmwarRegion = '-EU865'
            except:
                print('frimware region error')
                # ---- /Region Selection ----- #

            try:
                # ----- Firmware Downlaod URL----- #
                if values['-1.2.6-']:
                    binVersion = 'https://github.com/meshtastic/Meshtastic-device/releases/download/1.2.6/firmware-1.2.6.zip'
                elif values['-1.2.10-']:
                    binVersion = 'https://github.com/meshtastic/Meshtastic-device/releases/download/1.2.10/firmware-1.2.10.zip'
                elif values['-1.1.50-']:
                    binVersion = 'https://github.com/meshtastic/Meshtastic-device/releases/download/1.1.50/firmware-1.1.50.zip'
                elif values['-HN-']:
                    dateBuild = (time.strftime("%y-%m-%d"))
                    hamURL = 'http://www.casler.org/meshtastic/nightly_builds/meshtastic_device_nightly_'
                    binVersion = hamURL+'20'+dateBuild+'.zip'
            except:
                print('bin not pressent')
                # ----- /Firmware Download URL ----- #

            try:
                # ----- Donload Firmware File to zip ----- #
                url = binVersion
                firmwarefile = requests.get(url)
                open('firmware.zip', 'wb').write(firmwarefile.content)
                # ----- /Download Firmware File to zip ----- #

                # ---- Extract Frimware zip file ----- #
                with ZipFile('firmware.zip', 'r') as zipObj:
                    # Extract all the contents of zip file in current directory
                    zipObj.extractall(path='firmware')
                    #print(firmwareID+firmwarRegion)
            except:
                print(binVersion)

        # ----- Flash Firmware ----- #
        elif event == 'Flash Firmware': # this command requires .sh files be able to be handled by the system, windows can us
            try:
                # User browses for the file the y need and the file chose is used as input for the flashing script
                # script must be present in the parent folder in order for flash function to work
                os.system('sh device-install.sh -f '+values['_FILES_'])
            except:
                os.system('echo ERROR Flash Firmware Event >>error.log')
        # ----- /Flash Firmware ----- #

        # ----- Update firmware ----- #
        elif event == 'Update Firmware':# update firmware while keeping settings in place
            try:
                # User browses for the file the y need and the file chose is used as input for the flashing script
                # script must be present in the parent folder in order for flash function to work
                os.system('sh device-update.sh -f '+values['_FILES_'])
            except:
                os.system('echo ERROR Firmware update Event >>error.log')
        # ----- /Update firmware ----- #

        # ----- Set Wifi ----- #
        elif event == 'Set Wifi SSID':
            try:
                os.system('meshtastic  --set wifi_ssid '+values['-WifiSSID-'])
            except:
                print('error wifi ssid')

        elif event == 'Set Wifi Password':
            try:
                os.system('meshtastic  --set wifi_password '+values['-WifiPASS-'])
            except:
                print('error wifi password')

        # ----- /Set Wifi ---- #

        # ----- AP ON ----- #

        elif event == 'AP On':
            try:
                os.system('meshtastic --set wifi_ap_mode true')
            except:
                print('Error activating AP mode')
        # ----- /AP ON ----#

        # ----- AP off ----- #

        elif event == 'AP Off':
            try:
                os.system('meshtastic --set wifi_ap_mode false')
            except:
                print('Error trying to turn AP off ')
# end Loop

if __name__ == '__main__':
    main()
