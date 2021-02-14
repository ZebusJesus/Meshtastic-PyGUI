import PySimpleGUI as sg
import os
import requests
import meshtastic
import subprocess
from pubsub import pub
"""

    All windows are immediately visible.  Each window updates the other.

    There's an added capability to "re-open" window 2 should it be closed.  This is done by simply calling the make_win2VERSION function
    again when the button is pressed in window 1.

    The program exits when all windows have been closed

    Copyright 2020 PySimpleGUI.org
"""

def make_win1API():
    sg.theme('DarkAmber')
    layout = [[sg.Text('Welcome to the Meshtastic Python GUI!!  WARNING I AM NOT RESPONSIBLE FOR ERRORS OR BROKEN DEVICES, LOOK BEFORE YOUR RUN')],
              [sg.Button('Radio Information'), sg.Button('Help'), sg.Button('QR')],
              [sg.Text('Make sure to enclose message in " ", this allows for spaces in messages')],
              [sg.Button('Set Channel Settings'), sg.Text('SF'), sg.InputText(size=(10,1),key='-SFINPUT-'), sg.Text('CR'), sg.InputText(size=(10,1),key='-CRINPUT-'),
              sg.Text('BW'), sg.InputText(size=(10,1),key='-BWINPUT-')],
              [sg.Button('Set Long Slow'),sg.Button('Set Short Fast')],
              [sg.Button('Set URL'), sg.InputText(key='-URLINPUT-')],
              [sg.Button('Set Owner'), sg.InputText(key='-OWNERINPUT-')],
              [sg.Button('Set Lattitude'),sg.InputText(size=(10,1),key='-SETLAT-'), sg.Button('Set Longitude'), sg.InputText(size=(10,1),key='-SETLON-'),
              sg.Button('Set Altitude'), sg.InputText(size=(10,1),key='-SETALT-')],
              [sg.Button('Set Router'), sg.Button('Unset Router')],
              [sg.Button('Reopen2'), sg.Button('Reopen3')],
              [sg.Button('Exit')]
             ]
    return sg.Window('Meshtastic API', layout, finalize=True)


def make_win2VERSION():
    layout = [[sg.Text('Hardware and  Firmware build selection')],
               [sg.Checkbox('T-Beam',key='-T-Beam-'),sg.Checkbox('heltec',key='-heltec-'),
                sg.Checkbox('T-LoRa',key='-T-LoRa-'),sg.Checkbox('LoRa Relay',key='-LoRa Relay-')],
               [sg.Checkbox('ANZ'),sg.Checkbox('CN'),sg.Checkbox('EU865'),sg.Checkbox('EU443'),sg.Checkbox('JP'),sg.Checkbox('KR'),sg.Checkbox('US')],
               [sg.Checkbox('Stable'), sg.Checkbox('Beta'), sg.Checkbox('Alpha'), sg.Checkbox('Hamster Nightly')],
               [sg.Button('Download Firmware')],
               [sg.Input(key='_FILES_'), sg.FilesBrowse()],
               [sg.Text('Firmware festure not complete, the download just downloads the 1.33 binary to a test.zip')],
               [sg.Text('If you extract that folder you will find the binareies you need and you can browse to the')],
               [sg.Text('needed one using the browse button and then use the flash or update buttons.')],
               [sg.Button('Flash Firmware'), sg.Button('Update Firmware'), sg.Cancel()],
               [sg.Button('Exit')]
              ]
    return sg.Window('Firmware Utility', layout, finalize=True)

def make_win3():
    layout = [[sg.Text('Window 3')],
              #[sg.Text('Enter something to output to Window 1')],
              #[sg.Input(key='-IN-', enable_events=True)],
              #[sg.Text(size=(25,1), key='-OUTPUT-')],
              [sg.Output(size=(20,20))],
              [sg.Button('Send Message'), sg.InputText(key='-MSGINPUT-')],
              [sg.Button('Connect to Radio'), sg.Button('Exit'),sg.Button('Close Radio Connection')]]
    return sg.Window('Radio I/O', layout, finalize=True)

def radio_close():
    interface_close=meshtastic.SerialInterface()


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

        elif event == 'Close Radio Connection':
            output_window = window3

            #meshtastic.SreamInterface.close()

        elif event == 'Reopen2':
            if not window2:
                window2 = make_win2VERSION()
                window2.move(window1API.current_location()[0], window1API.current_location()[1] + 220)

        elif event == 'Reopen3':
            if not window3:
                window3 = make_win3()
                window3.move(window1API.current_location()[0], window1API.current_location()[1] - 220)

        elif event == '-IN-':
            output_window = window3 if window == window1API else window1API
            if output_window:           # if a valid window, then output to it
                output_window['-OUTPUT-'].update(values['-IN-'])
            else:
                window['-OUTPUT-'].update('Other window is closed')

        elif event == 'Connect to Radio':
            output_window = window3
            def onReceive(packet, interface): # called when a packet arrives
                print(f"Received: {packet}")

            def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
                # defaults to broadcast, specify a destination ID if you wish
                interface.sendText("hello mesh")

            pub.subscribe(onReceive, "meshtastic.receive")
            pub.subscribe(onConnection, "meshtastic.connection.established")
            # By default will try to find a meshtastic device, otherwise provide a device path like /dev/ttyUSB0
            interface = meshtastic.SerialInterface()


        elif event == 'Radio Information': #if user clicks Radio Information
            os.system("meshtastic --info >radioinfo.txt") # outout radio information to txt file

        elif event == 'Send Message': #if user clicks send message take input and send to radio
            os.system("meshtastic --sendtext "+ values['-MSGINPUT-'])

        elif event == 'Help':
            os.system("meshtastic -h && pause")

        elif event == 'QR':
            try:
                os.system("meshtastic --qr >QR.png")
            except:
                print('error')

        elif event == 'Set Channel':
            try:
                os.system("meshtastic --setchan spread_factor "+values['-SFINPUT-']+" --setchan coding_rate "+values['-CRINPUT-']+" --setchan bandwidth "+values['-BWINPUT-'])
            except:
                os.system("echo ERROR Set Channel Event >>error.log")
        elif event == 'Set URL':
            try:
                os.system("meshtatic --seturl "+values['-URLINPUT-'])
            except:
                os.system("echo ERROR Set URL error >>error.log")

        elif event == 'Set Long Slow':
            os.system("meshtastic --setch-longslow")

        elif event == 'Set Short Fast':
            os.system("meshtastic --setch-shortfast")

        elif event == 'Set Owner':
            os.system("meshtastic --setowner "+values['-OWNERINPUT-'])

        elif event == 'Set Lattitude':
            os.system("meshtastic --setlat "+values['-SETLAT-'])

        elif event == 'Set Longitude':
            os.system("meshtastic --setlon "+values['-SETLON-'])

        elif event == 'Set Altitude':
            os.system("meshtastic --setalt "+values['-SETALT-'])

        elif event == 'Set Router':
            os.system("echo meshtastic --setrouter")

        elif event == 'Unset Router':
            os.system("echo meshtastic --unset-router")

        elif event == 'Download Firmware':
            firmwareID = 'NULL'
            try:
                if event == values['-T-Beam-'] == True:
                    firmwareID = '-tbeam'
                elif event == values['-heltec-'] == True:
                    firmwareID = "-heltec"
                elif event == values['-T-LoRa-'] == True:
                    firmwareID = "-tlora"
                elif event == values['-LoRa Relay-'] == True:
                    firmwareID = "-lora-relay"
                url = 'https://github.com/meshtastic/Meshtastic-device/releases/download/1.1.33/firmware-1.1.33.zip'
                firmwarefile = requests.get(url)
                open('test.zip', 'wb').write(firmwarefile.content)
            except:
                print('error')
        elif event == "Flash Firmware": # this command requires .sh files be able to be handled by the system, windows can us
            try:
                os.system("sh device-install.sh -f "+values['_FILES_'])
            except:
                os.system("echo ERROR Flash Firmware Event >>error.log")
        elif event == "Update Firmware":# update firmware while keeping settings in place
            try:
                os.system("sh device-update.sh -f "+values['_FILES_'])
            except:
                os.system("echo ERROR Firmware update Event >>error.log")



if __name__ == '__main__':
    main()
