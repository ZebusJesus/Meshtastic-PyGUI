import PySimpleGUI as sg
import os
import requests
import meshtastic
import subprocess
import time
from pubsub import pub
from zipfile import ZipFile



#"""
#    All windows are immediately visible.  Each window updates the other.
#    Window1 - main Window
#    Window2 - Firmware Window
#    Window3 - Radio Window

#    Copyright 2021 Zebus Jesus
##"""

def make_win1API():  ##define window one layout and contents
    sg.theme('DarkAmber')
    layout = [[sg.Text('Welcome to the Meshtastic Python GUI!!  WARNING I AM NOT RESPONSIBLE FOR ERRORS OR BROKEN DEVICES, LOOK BEFORE YOUR RUN')],
              [sg.Button('Radio Information'), sg.Button('Help'), sg.Button('QR')],
              [sg.Text('Make sure to enclose message in " ", this allows for spaces in messages')],
              [sg.Button('Set Channel Settings'), sg.Text('SF'), sg.InputText(size=(10,1),key='-SFINPUT-'), sg.Text('CR'), sg.InputText(size=(10,1),key='-CRINPUT-'),
              sg.Text('BW'), sg.InputText(size=(10,1),key='-BWINPUT-')],
              [sg.Button('Set Long Slow'),sg.Button('Set Short Fast')],
              [sg.Button('Set URL'), sg.InputText(key='-URLINPUT-')],
              [sg.Button('Set Wifi'),sg.Text('Wifi SSID'),sg.InputText(size=(20,1),key='-WifiSSID-'),sg.Text('Wifi Password'),sg.InputText(size=(20,1),key='-WifiPASS-')],
              [sg.Button('Set Owner'), sg.InputText(key='-OWNERINPUT-')],
              [sg.Button('Set Lattitude'),sg.InputText(size=(10,1),key='-SETLAT-'), sg.Button('Set Longitude'), sg.InputText(size=(10,1),key='-SETLON-'),
              sg.Button('Set Altitude'), sg.InputText(size=(10,1),key='-SETALT-')],
              [sg.Button('Set Router'), sg.Button('Unset Router')],
              [sg.Button('Firmware Window'), sg.Button('Radio Window')],
              [sg.Button('Exit')]
             ]
    return sg.Window('Meshtastic API', layout, finalize=True)


def make_win2VERSION():  ##define Frimware Window loayout and conents
    layout = [[sg.Text('Hardware and  Firmware build selection')],
               [sg.Checkbox('T-Beam',key='-T-Beam-',enable_events=True),sg.Checkbox('heltec',key='-heltec-'),
                sg.Checkbox('T-LoRa',key='-T-LoRa-'),sg.Checkbox('LoRa Relay',key='-LoRa Relay-')],
               [sg.Checkbox('ANZ',key='-ANZ-'),sg.Checkbox('CN',key='-CN-'),sg.Checkbox('EU865',key='-EU865-'),sg.Checkbox('EU443',key='-EU443-'),sg.Checkbox('JP',key='-JP-'),sg.Checkbox('KR',key='-KR-'),sg.Checkbox('US',key='-US-')],
               [sg.Checkbox('1.1.48',key='-1.1.48-'), sg.Checkbox('1.1.33',key='-1.1.33-'), sg.Checkbox('Alpha'), sg.Checkbox('Hamster Nightly',key='-HN-')],
               [sg.Button('Download Firmware')],
               [sg.Input(key='_FILES_'), sg.FilesBrowse()],
               [sg.Text('Firmware festure not complete, the download just downloads the binary to a firmware.zip')],
               [sg.Text('and is extracted to a folder called firmware.')],
               [sg.Text('You can then browse to the needed binary in the firmware folder.')],
               [sg.Button('Flash Firmware'), sg.Button('Update Firmware'), sg.Cancel()],
               [sg.Button('Exit')]
              ]
    return sg.Window('Firmware Utility', layout, finalize=True)

def make_win3():  ##define Radio Window Layout and contents
    layout = [[sg.Text('Radio I/O')],
              #[sg.Text('Enter something to output to Window 1')],
              #[sg.Input(key='-IN-', enable_events=True)],
              #[sg.Text(size=(25,1), key='-OUTPUT-')],
              [sg.Output(size=(20,20),key='-OUTPUT_RADIO-')],
              [sg.Button('Send Message'), sg.InputText(key='-MSGINPUT-')],
              [sg.Button('Connect to Radio'), sg.Button('Exit'),sg.Button('Close Radio Connection')]]
    return sg.Window('Radio I/O', layout, finalize=True)

#try:
#    interface = meshtastic.SerialInterface()
#except:
#    print('No Radio Connected')

def main():
    window1API, window2, window3 = make_win1API(), make_win2VERSION(), make_win3()

    window2.move(window1API.current_location()[0], window1API.current_location()[1]+220)

    window3.move(window1API.current_location()[0], window1API.current_location()[1]+220)



    while True:             # Event Loop
        window, event, values = sg.read_all_windows()

        if window == sg.WIN_CLOSED:     # if all windows were closed
            break

        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            if window == window2:       # if closing win 2, mark as closed
                window2 = None
            elif window == window1API:     # if closing win 1, mark as closed
                window1API = None
            elif window == window3:
                window3 = None

        ##elif event == 'Close Radio Connection':
            #output_window = window3
            #os.system("devcon.exe hwids * >>hwid.txt")

            #meshtastic.SreamInterface.close()

        elif event == 'Firmware Window':
            if not window2:
                window2 = make_win2VERSION()
                window2.move(window1API.current_location()[0], window1API.current_location()[1] + 220)

        elif event == 'Radio Window':
            if not window3:
                window3 = make_win3()
                window3.move(window1API.current_location()[0], window1API.current_location()[1] - 220)

        elif event == '-IN-':
            output_window = window3
            if output_window:           # if a valid window, then output to it
                output_window['-OUTPUT-'].update(values['-IN-'])
            else:
                window['-OUTPUT-'].update('Other window is closed')

        elif event == 'Connect to Radio':
            output_window = window3
            ##interface = meshtastic.SerialInterface()
            def onReceive(packet, interface): # called when a packet arrives
                print(f'Received: {packet}')

            def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
                # defaults to broadcast, specify a destination ID if you wish
                meshtastic.SerialInterface().sendText('hello mesh')

            print(pub.subscribe(onReceive, 'meshtastic.receive'))
            print(pub.subscribe(onConnection, 'meshtastic.connection.established'))
            # By default will try to find a meshtastic device, otherwise provide a device path like /dev/ttyUSB0


        elif event == 'Radio Information': #if user clicks Radio Information
            os.system('meshtastic --info >radioinfo.txt') # outout radio information to txt file

        elif event == 'Send Message': #if user clicks send message take input and send to radio
            os.system('meshtastic --sendtext '+ values['-MSGINPUT-'])

        elif event == 'Help': #if user clicks the help button
            os.system('meshtastic -h && pause') #output meshtastic help via cmd prompt

        elif event == 'QR':#if user clicks QR button
            try:
                os.system('meshtastic --qr >QR.tmp')
            except:
                os.system('echo ERROR QR >>error.log')


        elif event == 'Set Channel': #if user clicks Set Channel button
            try:
                os.system('meshtastic --setchan spread_factor '+values['-SFINPUT-']+' --setchan coding_rate '+values['-CRINPUT-']+' --setchan bandwidth '+values['-BWINPUT-'])
            except:
                os.system('echo ERROR Set Channel Event >>error.log')
        elif event == 'Set URL':
            try:
                os.system('meshtatic --seturl '+values['-URLINPUT-'])
            except:
                os.system('echo ERROR Set URL error >>error.log')

        elif event == 'Set Long Slow':
            try:
                os.system('meshtastic --setch-longslow')
            except:
                os.system('echo ERROR Set Channel LongSlow >>error.log')

        elif event == 'Set Short Fast':
            try:
                os.system('meshtastic --setch-shortfast')
            except:
                os.system('echo ERROR Set Channel ShortFast >>error.log')


        elif event == 'Set Owner':
            os.system('meshtastic --setowner '+values['-OWNERINPUT-'])

        elif event == 'Set Lattitude':
            os.system('meshtastic --setlat '+values['-SETLAT-'])

        elif event == 'Set Longitude':
            os.system('meshtastic --setlon '+values['-SETLON-'])

        elif event == 'Set Altitude':
            os.system('meshtastic --setalt '+values['-SETALT-'])

        elif event == 'Set Router':
            os.system('meshtastic --setrouter')

        elif event == 'Unset Router':
            os.system('echo meshtastic --unset-router')

        elif event == 'Download Firmware':
            firmwareID = 'NULL'
            firmwarRegion = 'NULL'
            binVersion = 'NULL'
            try:
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

            try:
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

            try:
                if values['-1.1.48-']:
                    binVersion = 'https://github.com/meshtastic/Meshtastic-device/releases/download/1.1.48/firmware-1.1.48.zip'
                elif values['-1.1.33-']:
                    binVersion = 'https://github.com/meshtastic/Meshtastic-device/releases/download/1.1.33/firmware-1.1.33.zip'
                elif values['-HN-']:
                    dateBuild = (time.strftime("%y-%m-%d"))
                    hamURL = 'http://www.casler.org/meshtastic/nightly_builds/meshtastic_device_nightly_'
                    binVersion = hamURL+'20'+dateBuild+'.zip'
            except:
                print('bin not pressent')

            try:
                url = binVersion
                firmwarefile = requests.get(url)
                open('firmware.zip', 'wb').write(firmwarefile.content)

                with ZipFile('firmware.zip', 'r') as zipObj:
                # Extract all the contents of zip file in current directory

                    zipObj.extractall(path='firmware')
                    print(firmwareID+firmwarRegion)
            except:
                print(binVersion)

        elif event == 'Flash Firmware': # this command requires .sh files be able to be handled by the system, windows can us
            try:
                os.system('sh device-install.sh -f '+values['_FILES_'])
            except:
                os.system('echo ERROR Flash Firmware Event >>error.log')


        elif event == 'Update Firmware':# update firmware while keeping settings in place
            try:
                os.system('sh device-update.sh -f '+values['_FILES_'])
            except:
                os.system('echo ERROR Firmware update Event >>error.log')


        elif event == 'Set Wifi':
            try:
                os.system('meshtastic --set wifi_ap_mode false --setstr wifi_ssid '+values['-WifiSSID-']+' --setstr wifi_password '+values['-WifiPASS-'])
            except:
                print('error wifi ssid')





if __name__ == '__main__':
    main()
