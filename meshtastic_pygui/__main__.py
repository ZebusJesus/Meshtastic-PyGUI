# ----- <About> ----- #
#   Author: Zebus Zebus
#   Email: zebusjesus@pm.me
#   Date: 7-21-21
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
#from map3 import mapNODE

# ----- </IMports> ----- #

# ------ <Menu_Definition> ------ #

menu_def = [['&File', ['&Properties', 'E&xit']],
            ['GPS', ['Range Test', ['Download Range Data', 'Normal', ], 'Future Function'], ],
            ['&Toolbar', ['---', 'Firmware Window', 'Radio Window',
                          '---', 'Options', 'Nodes']],
            ['&Help', '&About...'], ]

# ----- </Menu Definition> ----- #

# ----- Window 1 ----- #
def make_win1API():
    sg.theme('DarkAmber')
    sg.set_options(element_padding=(1, 1))


    layout = [
              [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
              [sg.Text('Welcome to the Meshtastic Python GUI!!  WARNING I AM NOT RESPONSIBLE FOR ERRORS OR BROKEN DEVICES, LOOK BEFORE YOU RUN')],
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
              [sg.Button('Firmware Window'), sg.Button('Radio Window'),sg.Button('Options'),sg.Button('Node Window')],
              [sg.Button('Close')]
             ]

    return sg.Window('Meshtastic API', layout, finalize=True, no_titlebar=True, grab_anywhere=True)
# ----- /Window 1 ----- #

# ----- Window 2 ----- #
def make_win2FIRMWARE():  ##define Frimware Window loayout and conents
    sg.theme('DarkAmber')
    sg.set_options(element_padding=(1, 1))
    layout = [
               [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
               [sg.Text('Hardware and  Firmware build selection')],
               [sg.Checkbox('T-Beam',key='-T-Beam-',enable_events=True),sg.Checkbox('heltec',key='-heltec-'),
                sg.Checkbox('T-LoRa',key='-T-LoRa-'),sg.Checkbox('LoRa Relay',key='-LoRa Relay-')],
               [sg.Checkbox('1.2.42',key='-1.2.42-'), sg.Checkbox('1.2.38',key='-1.2.38-'), sg.Checkbox('1.2.28',key='-1.2.28-'), sg.Checkbox('Hamster Nightly',key='-HN-')],
               [sg.Button('Download Firmware')],
               [sg.Text('Firmware'),sg.Input(key='_FILES_'), sg.FilesBrowse()],
               [sg.Text('spiff'),sg.Input(key='_FILES2_'), sg.FilesBrowse()],
               [sg.Text('system-info'),sg.Input(key='_FILES3_'), sg.FilesBrowse()],
               [sg.Text('You can then browse to the needed binary in the firmware folder.')],
               [sg.Text('Flashing Firmware requires you select a firmware, spiff and system-info file locations')],
               [sg.Button('Flash Firmware'), sg.Button('Update Firmware'), sg.Button('Erase Firmware')],
               [sg.Button('Backup Firmware'),sg.Input(key='_BACKUP_FILE_')],
               [sg.Button('Restore Frimware'),sg.Input(key='_RESTORE_FILE_'),sg.FilesBrowse()],
               [sg.Button('Close'), sg.Cancel()]
              ]
    return sg.Window('Firmware Utility', layout, finalize=True, no_titlebar=True, grab_anywhere=True)
# ------ /Window 2 ------ #

# ----- Radio I/O Window ----- #

def make_win3RADIO():  ##define Radio Window Layout and contents

    sg.theme('DarkAmber')
    sg.set_options(element_padding=(1, 1))
    layout = [
             [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
             [sg.Text('Radio I/O')],
             [sg.Output(size=(80,25),key='-OUTPUT_RADIO-')],
             [sg.Button('Send Message to all',key='Send Message'), sg.InputText(key='-MSGINPUT-'),sg.Checkbox('AK MSK',key='-AKMSGTF-'),
             sg.Checkbox('Want Response',key='-WNTRSPTF-')],
             [sg.Button('Send to node'),sg.Text('message'),sg.InputText(size=(20,1),key='-NODE_MSG-'),
                sg.Text('Node'),sg.InputText(size=(10,1),key='-NODE-')],
             [sg.Button('Connect to Radio'), sg.Button('Close Radio Window'),sg.Button('Close Radio Connection')]]
    return sg.Window('Radio I/O', layout, finalize=True, no_titlebar=True, grab_anywhere=True)

# ----- /Radio I/O Window -----#

# ---- Nodes Window ----- #
def make_win5NODES():  ##define Radio Window Layout and contents

    sg.theme('DarkAmber')
    sg.set_options(element_padding=(1, 1))
    layout = [
             [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
             [sg.Text('Nodes')],
             [sg.Output(size=(100,25),key='-OUTPUT_NODES-')],
             [sg.Button('Nodes')],
             [sg.Button('Send Message to node'),sg.Text('message'),sg.InputText(size=(20,1),key='-NODE_MSG-'),
                sg.Text('Node'),sg.InputText(size=(10,1),key='-NODE-')],
             [sg.Button('Send Command to node'),sg.Text('command'),sg.InputText(size=(20,1),key='-NODE_CMD-'),
               sg.Text('Node'),sg.InputText(size=(10,1),key='-NODE1-')],
             [sg.Button('Close Node Window')]
             ]

    return sg.Window('Nodes', layout, finalize=True, no_titlebar=True, grab_anywhere=True)
# ----- /Nodes Window ----- ##

# ----- Radio Option List Window ----- #
def make_win4OPTIONS():

    sg.theme('DarkAmber')
    sg.set_options(element_padding=(1, 1))
    layout = [
                [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
                [sg.Text('What Setting do you want to change?')],
                [sg.Listbox(values=['position_broadcast_secs','send_owner_interval','wait_bluetooth_secs','screen_on_secs',
                'phone_timeout_secs','phone_sds_timeout_sec','mesh_sds_timeout_secs','sds_secs',
                'ls_secs','min_wake_secs','wifi_ssid','wifi_password','wifi_ap_mode','region',
                'charge_current','is_router','is_low_power','fixed_position','factory_reset',
                'debug_log_enabled','location_share','gps_operation','gps_update_interval',
                'gps_attempt_time','ignore_incoming','serialplugin_enabled','serialplugin_echo',
                'serialplugin_rxd','serialplugin_txd','serialplugin_timeout','serialplugin_mode',
                'ext_notification_plugin_enabled','ext_notification_plugin_output_ms',
                'ext_notification_plugin_output','ext_notification_plugin_active',
                'ext_notification_plugin_alert_message','ext_notification_plugin_alert_bell',
                'range_test_plugin_enabled','range_test_plugin_sender','range_test_plugin_save',
                'store_forward_plugin_enabled','store_forward_plugin_records','environmental_measurement_plugin_measurement_enabled',
                'environmental_measurement_plugin_screen_enabled','environmental_measurement_plugin_read_error_count_threshold',
                'environmental_measurement_plugin_update_interval','environmental_measurement_plugin_recovery_interval',
                'environmental_measurement_plugin_display_farenheit','environmental_measurement_plugin_sensor_type',
                'environmental_measurement_plugin_sensor_pin'], size=(80, 20), key='-OPTION-')],
                [sg.Checkbox('Port Config'),sg.InputText(size=(20,1),key='-SETPORT-')],
                [sg.Button('Send Config --CAREFUL NOW--'),sg.InputText(size=(20,1),key='-SETVAL-')],
                [sg.Button('Close')] ]

    return sg.Window('Pick a Setting', layout, finalize=True,no_titlebar=True,grab_anywhere=True)
# ----- /Radio Option List Window ----- #


# ----- Draw_Windows ----- #
def main():
    window5NODES, windows2FIRMWARE, window3RADIO, window1API = make_win5NODES(), make_win2FIRMWARE(), make_win3RADIO(), make_win1API()

    windows2FIRMWARE.move(window1API.current_location()[0]-220, window1API.current_location()[1]+220)

    window3RADIO.move(window1API.current_location()[0]+620, window1API.current_location()[1]+20)

    output_window = window3RADIO

    #window4OPTIONS.move(window1API.current_location()[0]+420, window1API.current_location()[1]+20)

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
            elif window == window4OPTIONS:
                window4OPTIONS = None
            elif window == window5NODES:
                window5NODES = None

        elif event == "Close Node Window":
            window5NODES.close()

        elif event == "Close Radio Window":
            window3RADIO.close()

# ------ /Close Windows and programs ----- #

# ----- Menu About ----- #
        elif event == 'About...':
            sg.popup('version 2.7.3')
# ----- /Menu About ----- #

# ----- Open ----- #


# ----- /Open ----- #

# ----- Properties ----- #
        elif event == 'Properties':
            try:
                output_window = window3RADIO
                os.system('python -m meshtastic --info >radioinfo.txt')
                f = open('radioinfo.txt', 'r')
                file_contents = f.read()
                sg.popup(print(file_contents))
            except Exception:
                sg.popup('No Device Present')
# ----- /Properties ----- #

        elif event == 'Close Radio Connection':

            #os.system("devcon.exe hwids * >>hwid.txt")
            try:
                output_window = window3RADIO
                interface = meshtastic.SerialInterface()
                interface.close()
                print('closing connection to radio')
            except Exception:
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
                sg.popup("Error connecting to radio")
# ---- /Open COM connection to Radio ----- #

# ----- Get Radio info ----- #
        elif event == 'Radio Information': #if user clicks Radio Information
            try:
                os.system('python -m meshtastic --info >radioinfo.txt') # outout radio information to txt file
            except Exception:
                sg.popup('Error getting radio info')
# ----- /Get Raadio info ---- #

# ----- Send Message ----- #
        elif event == 'Send Message': #if user clicks send message take input and send to radio

            try:
                interface = meshtastic.SerialInterface()
                interface.sendText(values['-MSGINPUT-'],
                 wantAck=values['-AKMSGTF-'],
                 wantResponse=values['-WNTRSPTF-'],
                 onResponse=None)
                interface.close()
            except Exception:
                output_window = window3RADIO
                sg.popup('Error sending message')
# ----- /Send Message ----- #

        elif event == 'Send Message to node':
            try:
                os.system('python -m meshtastic --dest '+ values['-NODE-']+' --sendtext '+values['-NODE_MSG-'])
            except Exception:
                sg.popup('Error sending message to '+values['-NODE-'])

# ----- Send Command ----- #

        elif event == 'Send Command to node':
            try:
                os.system('python -m meshtastic --dest '+ values['-NODE1-']+' '+values['-NODE_CMD-'] )
            except Exception:
                sg.popup('Error sending command to '+values['-NODE1-'])

# ----- /Send Command ----- #

# ----- Help ----- #
        elif event == 'Help':
            output_window = window3RADIO
             #if user clicks the help button
            os.system('python -m meshtastic -h >help.txt')
            help_read = open('help.txt') #output meshtastic help via cmd prompt
            rh= help_read.read()
            print(rh)

# ----- QR ----- #
        elif event == 'QR':#if user clicks QR button
            try:
                os.system('python -m meshtastic --qr >QR.tmp')
            except Exception:
                os.system('echo ERROR QR >>error.log')
# ----- /QR ------ #

# ------ Set Channel -----#
        elif event == 'Set Channel': #if user clicks Set Channel button
            try:
                os.system('python -m meshtastic --setchan spread_factor '+values['-SFINPUT-']+' --setchan coding_rate '+values['-CRINPUT-']+' --setchan bandwidth '+values['-BWINPUT-'])
            except Exception:
                sg.popup('Error setting channel')
                os.system('echo ERROR Set Channel Event >>error.log')
# ------ /Set Channel ----- #

# ----- Set URL ----- #
        elif event == 'Set URL':
            try:
                os.system('python -m meshtastic --seturl '+values['-URLINPUT-'])
            except Exception:
                sg.popup('Error setting url')
                os.system('echo ERROR Set URL error >>error.log')
# ----- /Set URL ----- #

# ----- Set Long Slow ----- #
        elif event == 'Set Long Slow':
            try:
                os.system('python -m meshtastic --setch-longslow')
            except Exception:
                sg.popup('Error')
                os.system('echo ERROR Set Channel LongSlow >>error.log')
# ------ /Set Long Slow ----- #

# ----- Set Short Fast ----- #
        elif event == 'Set Short Fast':
            try:
                os.system('python -m meshtastic --setch-shortfast')
            except Exception:
                sg.popup('Error')
                os.system('echo ERROR Set Channel ShortFast >>error.log')
# ----- /Set Shor Fast ----- #

# ----- Set Owner ----- #
        elif event == 'Set Owner':
            try:
                os.system('python -m meshtastic --setowner '+values['-OWNERINPUT-'])
            except Exception:
                sg.popup('Error')
# ----- /Set Owner ----- #

# ----- Set Lattitude -----#
        elif event == 'Set Lattitude':
            try:
                os.system('python -m meshtastic --setlat '+values['-SETLAT-'])
            except Exception:
                sg.popup('Error')
# ----- /Set Lattitude ----- #

# ----- Set Longitude ----- #
        elif event == 'Set Longitude':
            try:
                os.system('python -m meshtastic --setlon '+values['-SETLON-'])
            except Exception:
                sg.popup('Error')
# ----- /Set Longitude ----- #

# ----- Set Altitude ----- #
        elif event == 'Set Altitude':
            try:
                os.system('python -m meshtastic --setalt '+values['-SETALT-'])
            except Exception:
                sg.popup('Error')
# -----/ Set Altitude ----- #

# ----- Set Router ----- #
        elif event == 'Set Router':
            os.system('python -m meshtastic --set is_router true')
# ----- /Set Router ----- #

# ----- Unset Router ----- #
        elif event == 'Unset Router':
            os.system('python -m meshtastic --set is_router false')
# ----- /Unset Router ----- #

# ----- Download Firmware ----- #
        elif event == 'Download Firmware':
            firmwareID = 'NULL'
            firmwarRegion = 'NULL'
            binVersion = 'NULL'
            try:
                # ----- Firmware Downlaod URL----- #
                if values['-1.2.47-']:
                    binVersion = 'https://github.com/meshtastic/Meshtastic-device/releases/download/v1.2.47/firmware-1.2.47.zip'
                elif values['-1.2.48-']:
                    binVersion = 'https://github.com/meshtastic/Meshtastic-device/releases/download/v1.2.48.371335e/firmware-1.2.48.371335e.zip'
                elif values['-1.2.42-']:
                    binVersion = 'https://github.com/meshtastic/Meshtastic-device/releases/download/v1.2.42.2759c8d/firmware-1.2.42.2759c8d.zip'
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
            except Exception:
                sg.popup('error exctracting bin')
                os.system('echo exrror extracting bin >>error.log')
                #print('error extarcting bin')

        # ----- Flash Firmware ----- #
        elif event == 'Flash Firmware': # this command requires .sh files be able to be handled by the system, windows can us
            try:
                os.system('python -m esptool --baud 921600 erase_flash')
                os.system('python -m esptool --baud 921600 write_flash 0x1000 '+values['_FILES3_'])
                os.system('python -m esptool --baud 921600 write_flash 0x00390000 '+values['_FILES2_'])
                os.system('python -m esptool --baud 921600 write_flash 0x10000 '+values['_FILES_'])
            except Exception:
                sg.popup('Flash Error')
                os.system('echo ERROR Flash Firmware Event >>error.log')
        # ----- /Flash Firmware ----- #

        # ----- Update firmware ----- #
        elif event == 'Update Firmware':# update firmware while keeping settings in place
            try:
                # User browses for the file the y need and the file chose is used as input for the flashing script
                # script must be present in the parent folder in order for flash function to work
                # os.system('sh device-update.sh -f '+values['_FILES_'])
                os.system('python -m esptool --baud 921600 write_flash 0x10000 '+values['_FILES_'] )
            except Exception:
                sg.popup('Firmware update error')
                os.system('echo ERROR Firmware update Event >>error.log')
        # ----- /Update firmware ----- #

        # ----- Erase Firmware ----- #
        elif event == 'Erase Firmware':
            try:
                os.system('python -m esptool --baud 921600 erase_flash')
            except Exception:
                sg.popup(' Erase Flash Error')
                os.system('echo ERROR Erasing Flash Firmware Event >>error.log')
        # ----- /Erase Firmware ----- #

        # ----- Backup Firmware ----- #
        elif event == 'Backup Firmware':
            try:
                os.system('python -m esptool --baud 921600 read_flash 0x00000 0x400000 '+values['_BACKUP_FILE_'])
            except Exception:
                sg.popup('Backup Error')
                os.system('echo ERROR Backup Firmware Event >>error.log')
        # ----- /Backup Firmware ----- #

        # ----- Restore Friimware ---- #

        elif event == 'Restore Firmware':
            try:
                os.system('python -m esptool --baud 921600 write_flash --flas_freq 80m 0x000000 '+values['_RESTORE_FILE_'])
            except Exception:
                output_window = window3RADIO
                sg.popup('Restore Flash Error')
                os.system('echo ERROR Restore Flash Firmware Event >>error.log')
        # ----- /Restore Firmware ----- #

        # ----- Set Wifi ----- #
        elif event == 'Set Wifi SSID':
            try:
                os.system('python -m meshtastic  --set wifi_ssid '+values['-WifiSSID-'])
            except Exception:
                sg.popup('Wifi Setting Error')
                os.system('echo ERROR setting SSID >>error.log')

        elif event == 'Set Wifi Password':
            try:
                os.system('python -m meshtastic  --set wifi_password '+values['-WifiPASS-'])
            except Exception:
                sg.popup('Wifi Password Error')
                os.system('echo ERROR setting wifi password e Event >>error.log')

        # ----- /Set Wifi ---- #

        # ----- AP ON ----- #

        elif event == 'AP On':
            try:
                os.system('python -m meshtastic --set wifi_ap_mode true')
            except Exception:
                sg.popup('Error activating AP mode')
                os.system('echo ERROR setting AP on Event >>error.log')
        # ----- /AP ON ----#

        # ----- AP off ----- #

        elif event == 'AP Off':
            try:
                os.system('python -m meshtastic --set wifi_ap_mode false')
            except Exception:
                sg.popup('Error trying to turn AP o ff ')

        # ----- /AP Off ----- #

        # ----- Factory Reset ----- #
        elif event == 'Factory Reset':
            try:
                os.system('python -m meshtastic --set factory_reset true')
            except Exception:
                sg.popup('Error Resetting Radio ')


# ----- <Option WIndow> ----- #
        elif event == 'Options':
            window4OPTIONS = make_win4OPTIONS()

        elif event == 'Send Config --CAREFUL NOW--':
            output_window = window3RADIO
            try:
                if values['-OPTION-']:    # if something is highlighted in the list
                    sg.popup(f" WARNING Command being sent: python -m meshtastic --set {values['-OPTION-'][0]} {values['-SETVAL-']}",
                    "WARNING Disconnect your radio now if you do not want this setting to be changed")
                    set_option_var = values['-OPTION-'][0]
                    set_option_val = values['-SETVAL-']
                    set_option_port = values['-SETPORT-']
                    print('python -m meshtastic --set '+set_option_var+' '+set_option_val)
                    try:
                        os.system('python -m meshtastic --set '+set_option_var+' '+set_option_val)
                    except Exception:
                        print('error connecting to radio')
            except Exception:
                print("error applying setting")
# -----</Options Window> ------ #

        elif event == 'Nodes':
            try:
                os.system('python -m meshtastic --nodes')
                n = open('nodes.txt', 'r')
                file_contents = n.read()
                print(file_contents)
            except Exception:
                print('error listing nodes')

        elif event == 'Node Window':
            window5NODES = make_win5NODES()


        elif event == 'Download Range Data':
            try:
                rangetest = requests.get('http://192.168.42.1/static/rangetest.csv')
                open('rangetest1.csv', 'wb').write(rangetest.content)
            except Exception:
                sg.popup('Error downloading range test data')
# end Loops

if __name__ == '__main__':
    main()
