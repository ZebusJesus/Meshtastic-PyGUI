# ----- <About> ----- #
#   Author: Zebus Zebus
#   Email: zebusjesus@pm.me
#   Date: 3-13-21
#   Meshtastic PyGUI
#   Thank you to all the members of meshtastic that make this project possible
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

# ----- </IMports> ----- #

# ------ <Menu_Definition> ------ #

menu_def = [['&File', ['&Properties', 'E&xit']],
            ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Toolbar', ['---', 'Firmware Window', 'Radio Window',
                          '---', 'Command &3', 'Command &4']],
            ['&Help', '&About...'], ]

# ----- </Menu Definition> ----- #

# ----- Window 1 ----- #
def make_win1API():
    sg.theme('DarkAmber')
    sg.set_options(element_padding=(1, 1))


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
              [sg.Button('Factory Reset')],
              [sg.Button('Firmware Window'), sg.Button('Radio Window')],
              [sg.Button('Close')]
             ]
    return sg.Window('Meshtastic API', layout, finalize=True, no_titlebar=True, grab_anywhere=True)
# ----- /Window 1 ----- #

# ----- Window 2 ----- #
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
               [sg.Button('Flash Firmware'), sg.Button('Update Firmware'), sg.Button('Erase Firmware')],
               [sg.Button('Close'), sg.Cancel()]
              ]
    return sg.Window('Firmware Utility', layout, finalize=True, no_titlebar=True, grab_anywhere=True)
# ------ /Window 2 ------ #
# ----- Radio I/O Window ----- #

def make_win3RADIO():  ##define Radio Window Layout and contents
    layout = [
             [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
             [sg.Text('Radio I/O')],
             [sg.Output(size=(80,25),key='-OUTPUT_RADIO-')],
             [sg.Button('Send Message to all',key='Send Message'), sg.InputText(key='-MSGINPUT-')],
             [sg.Button('Send to node'),sg.Text('message'),sg.InputText(size=(20,1),key='-NODE_MSG-'),
                sg.Text('Node'),sg.InputText(size=(10,1),key='-NODE-')],
             [sg.Button('Connect to Radio'), sg.Button('Close'),sg.Button('Close Radio Connection')]]
    return sg.Window('Radio I/O', layout, finalize=True, no_titlebar=True)

    # ----- /Radio I/O Window -----#


# ----- Draw_Windows ----- #
def window_event_loop():
    window1API, windows2FIRMWARE, window3RADIO = make_win1API(), make_win2FIRMWARE(), make_win3RADIO()

    windows2FIRMWARE.move(window1API.current_location()[0]-220, window1API.current_location()[1]+220)

    window3RADIO.move(window1API.current_location()[0]+620, window1API.current_location()[1]+20)
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
            if window == windows2FIRMWARE:       # if closing win 2, mark as closed
                windows2FIRMWARE = None
            elif window == window1API:     # if closing win 1, mark as closed
                window1API = None
            elif window == window3RADIO:
                window3RADIO = None
# ------ /Close Windows and programs ----- #

# ----- Menu About ----- #
        elif event == 'About...':
            window.disappear()
            sg.popup('About this program', 'Version 2.2.3',
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
            except Exception:
                output_window = window3RADIO
                sg.popup('No Device Present')
# ----- /Properties ----- #

        elif event == 'Close Radio Connection':

            #os.system("devcon.exe hwids * >>hwid.txt")
            try:
                output_window = window3RADIO
                meshtastic.SerialInterface().close(self)
            except Exception:
                output_window = window3RADIO
                sg.popup('Error Closing Serial Connection')

# ----- Open Firmware Window ----- #
        elif event == 'Firmware Window':
            if not windows2FIRMWARE:
                windows2FIRMWARE = make_win2FIRMWARE()
                windows2FIRMWARE.move(window1API.current_location()[0], window1API.current_location()[1] + 220)
# ----- /Open firmware Window ----- #

# ----- Open Radio I/O Window ----- #
        elif event == 'Radio Window':
            if not window3RADIO:
                window3RADIO = make_win3RADIO()
                window3RADIO.move(window1API.current_location()[0], window1API.current_location()[1] - 220)
# ----- /Open Radio I/O Window ----- #


# ----- Open COM connection to Radio ----- #
        elif event == 'Connect to Radio':
            try:
                output_window = window3RADIO
                interface = meshtastic.SerialInterface()
                def onReceive(packet, interface): # called when a packet arrives
                    print(f'Received: {packet}')

                def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
                    # defaults to broadcast, specify a destination ID if you wish
                    meshtastic.SerialInterface().sendText('hello mesh')

                print(pub.subscribe(onReceive, 'meshtastic.receive'))
                print(pub.subscribe(onConnection, 'meshtastic.connection.established'))
                # By default will try to find a meshtastic device, otherwise provide a device path like /dev/ttyUSB0
            except Exception:
                output_window = window3RADIO
                print("Error connecting to radio")
# ---- /Open COM connection to Radio ----- #

# ----- Get Radio info ----- #
        elif event == 'Radio Information': #if user clicks Radio Information
            try:
                os.system('meshtastic --info >radioinfo.txt') # outout radio information to txt file
            except Exception:
                output_window = window3RADIO
                sg.popup('Error getting radio info')
# ----- /Get Raadio info ---- #

# ----- Send Message ----- #
        elif event == 'Send Message': #if user clicks send message take input and send to radio
            try:
                os.system('meshtastic --sendtext '+ values['-MSGINPUT-'])
            except Exception:
                output_window = window3RADIO
                sg.popup('Error sending message')
# ----- /Send Message ----- #

        elif event == 'Send Message to node':
            try:
                os.system('meshtastic --dest '+ values['-NODE-']+' --sendtext '+values['-NODE_MSG-'])
            except Exception:
                output_window = window3RADIO
                sg.popup('Error sending message to '+values['-NODE-'])
# ----- Help ----- #
        elif event == 'Help':
            output_window = window3RADIO
             #if user clicks the help button
            os.system('meshtastic -h >help.txt')
            help_read = open('help.txt') #output meshtastic help via cmd prompt
            rh= help_read.read()
            print(rh)

# ----- QR ----- #
        elif event == 'QR':#if user clicks QR button
            try:
                os.system('meshtastic --qr >QR.tmp')
            except Exception:
                output_window = window3RADIO
                os.system('echo ERROR QR >>error.log')
# ----- /QR ------ #

# ------ Set Channel -----#
        elif event == 'Set Channel': #if user clicks Set Channel button
            try:
                os.system('meshtastic --setchan spread_factor '+values['-SFINPUT-']+' --setchan coding_rate '+values['-CRINPUT-']+' --setchan bandwidth '+values['-BWINPUT-'])
            except Exception:
                output_window = window3RADIO
                sg.popup('Error setting channel')
                os.system('echo ERROR Set Channel Event >>error.log')
# ------ /Set Channel ----- #

# ----- Set URL ----- #
        elif event == 'Set URL':
            try:
                os.system('meshtastic --seturl '+values['-URLINPUT-'])
            except Exception:
                output_window = window3RADIO
                sg.popup('Error setting url')
                os.system('echo ERROR Set URL error >>error.log')
# ----- /Set URL ----- #

# ----- Set Long Slow ----- #
        elif event == 'Set Long Slow':
            try:
                os.system('meshtastic --setch-longslow')
            except Exception:
                os.system('echo ERROR Set Channel LongSlow >>error.log')
# ------ /Set Long Slow ----- #

# ----- Set Short Fast ----- #
        elif event == 'Set Short Fast':
            try:
                os.system('meshtastic --setch-shortfast')
            except Exception:
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
            except Exception:
                sg.popup('bin not pressent')
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
            except Exception:
                print(binVersion)

        # ----- Flash Firmware ----- #
        elif event == 'Flash Firmware': # this command requires .sh files be able to be handled by the system, windows can us
            try:
                # User browses for the file the y need and the file chose is used as input for the flashing script
                # script must be present in the parent folder in order for flash function to work
                # os.system('sh device-install.sh -f '+values['_FILES_'])

                os.system('esptool.py --baud 921600 erase_flash')
                os.system('esptool.py --baud 921600 write_flash 0x1000 system-info.bin')
                os.system('esptool.py --baud 921600 write_flash 0x00390000 spiffs-*.bin')
                os.system('esptool.py --baud 921600 write_flash 0x10000 '+values['_FILES_'])

            except Exception:
                os.system('echo ERROR Flash Firmware Event >>error.log')
        # ----- /Flash Firmware ----- #

        # ----- Update firmware ----- #
        elif event == 'Update Firmware':# update firmware while keeping settings in place
            try:
                # User browses for the file the y need and the file chose is used as input for the flashing script
                # script must be present in the parent folder in order for flash function to work
                # os.system('sh device-update.sh -f '+values['_FILES_'])
                os.system('esptool.py --baud 921600 write_flash 0x10000 '+values['_FILES_'] )
            except Exception:
                os.system('echo ERROR Firmware update Event >>error.log')
        # ----- /Update firmware ----- #

        elif event == 'Erase Firmware':
            try:
                os.system('esptool.py --baud 921600 erase_flash')
            except Exception:
                sg.popup('error erasing firmware')

        # ----- Set Wifi ----- #
        elif event == 'Set Wifi SSID':
            try:
                os.system('meshtastic  --set wifi_ssid '+values['-WifiSSID-'])
            except Exception:
                sg.popup('error wifi ssid')

        elif event == 'Set Wifi Password':
            try:
                os.system('meshtastic  --set wifi_password '+values['-WifiPASS-'])
            except Exception:
                sg.popup('error wifi password')

        # ----- /Set Wifi ---- #

        # ----- AP ON ----- #

        elif event == 'AP On':
            try:
                os.system('meshtastic --set wifi_ap_mode true')
            except Exception:
                sg.popup('Error activating AP mode')
        # ----- /AP ON ----#

        # ----- AP off ----- #

        elif event == 'AP Off':
            try:
                os.system('meshtastic --set wifi_ap_mode false')
            except Exception:
                sg.popup('Error trying to turn AP o ff ')

        # ----- /AP Off ----- #

        # ----- Factory Reset ----- #
        elif event == 'Factory Reset':
            try:
                os.system('meshtastic --set factory_reset true')
            except Exception:
                sg.popup('Error Resetting Radio ')


# end Loops

if __name__ == '__main__':
    window_event_loop()
