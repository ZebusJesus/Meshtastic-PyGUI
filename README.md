# Meshtastic-PyGUI
A python Based GUI that uses the Meshtastic API


# Dependencies
python 3.7 or above
pip -- for install python Modules
Meshtastic 1.2.6   pip install --update Meshtastic
PySimpleGUI --  pip install PySimpleGUI


```
Python Modules:
  Meshtaestic
  PySimpleGUI
  os
  requests
  subprocess
  time
  zipfile
  esptool
```

## Install Commands 
```
Windows:

python -m pip install --upgrade meshtastic-pygui

OSX

pip3 install --upgrade meshtastic-pygui

Linux 

pip3 install --upgrade meshtastic-pygui
```

## Launch Command
```
Windows:

python -m meshtastic_pygui

MacOS:

python3 -m meshtastic_pygui
```

## A note for developers of this tool

If you need to build a new release you'll need:
```
Linux:
sudo pip3 install markdown twine

Windows 

python -m pip install markdown twine 
```

```
Windows users should note that the way windows handles COM ports is not the same as other systems.  If ran as admin "READ THE CODE BEFORE YOU RUN" then it is not an issue but if running as a normal user profile then you will have to unplug and plug the radio back in, this will release the COM port and make a new connection.  This limitation can cause the GUI to crash if the connection to the radio hangs.
```

Edit setup.py to have your new version number before each release (then check that change into github)

To test release the build to pypi run 'bin/test-release.sh' (or look at that file to see what you need to do on your operating system).  You should see something like this.  If all goes well it should look like this.

```
~/development/meshtastic/Meshtastic-PyGUI$ bin/test-release.sh
running sdist
running egg_info
writing meshtastic_pygui.egg-info/PKG-INFO
writing dependency_links to meshtastic_pygui.egg-info/dependency_links.txt
writing entry points to meshtastic_pygui.egg-info/entry_points.txt
writing requirements to meshtastic_pygui.egg-info/requires.txt
writing top-level names to meshtastic_pygui.egg-info/top_level.txt
reading manifest file 'meshtastic_pygui.egg-info/SOURCES.txt'
writing manifest file 'meshtastic_pygui.egg-info/SOURCES.txt'
running check
creating meshtastic_pygui-0.1.2
creating meshtastic_pygui-0.1.2/meshtastic_pygui
creating meshtastic_pygui-0.1.2/meshtastic_pygui.egg-info
copying files to meshtastic_pygui-0.1.2...
copying README.md -> meshtastic_pygui-0.1.2
copying setup.py -> meshtastic_pygui-0.1.2
copying meshtastic_pygui/__init__.py -> meshtastic_pygui-0.1.2/meshtastic_pygui
copying meshtastic_pygui/__main__.py -> meshtastic_pygui-0.1.2/meshtastic_pygui
copying meshtastic_pygui.egg-info/PKG-INFO -> meshtastic_pygui-0.1.2/meshtastic_pygui.egg-info
copying meshtastic_pygui.egg-info/SOURCES.txt -> meshtastic_pygui-0.1.2/meshtastic_pygui.egg-info
copying meshtastic_pygui.egg-info/dependency_links.txt -> meshtastic_pygui-0.1.2/meshtastic_pygui.egg-info
copying meshtastic_pygui.egg-info/entry_points.txt -> meshtastic_pygui-0.1.2/meshtastic_pygui.egg-info
copying meshtastic_pygui.egg-info/requires.txt -> meshtastic_pygui-0.1.2/meshtastic_pygui.egg-info
copying meshtastic_pygui.egg-info/top_level.txt -> meshtastic_pygui-0.1.2/meshtastic_pygui.egg-info
Writing meshtastic_pygui-0.1.2/setup.cfg
Creating tar archive
removing 'meshtastic_pygui-0.1.2' (and everything under it)
running bdist_wheel
running build
running build_py
creating build
creating build/lib
creating build/lib/meshtastic_pygui
copying meshtastic_pygui/__init__.py -> build/lib/meshtastic_pygui
copying meshtastic_pygui/__main__.py -> build/lib/meshtastic_pygui
installing to build/bdist.linux-x86_64/wheel
running install
running install_lib
creating build/bdist.linux-x86_64
creating build/bdist.linux-x86_64/wheel
creating build/bdist.linux-x86_64/wheel/meshtastic_pygui
copying build/lib/meshtastic_pygui/__init__.py -> build/bdist.linux-x86_64/wheel/meshtastic_pygui
copying build/lib/meshtastic_pygui/__main__.py -> build/bdist.linux-x86_64/wheel/meshtastic_pygui
running install_egg_info
Copying meshtastic_pygui.egg-info to build/bdist.linux-x86_64/wheel/meshtastic_pygui-0.1.2.egg-info
running install_scripts
adding license file "LICENSE" (matched pattern "LICEN[CS]E*")
creating build/bdist.linux-x86_64/wheel/meshtastic_pygui-0.1.2.dist-info/WHEEL
creating 'dist/meshtastic_pygui-0.1.2-py3-none-any.whl' and adding 'build/bdist.linux-x86_64/wheel' to it
adding 'meshtastic_pygui/__init__.py'
adding 'meshtastic_pygui/__main__.py'
adding 'meshtastic_pygui-0.1.2.dist-info/LICENSE'
adding 'meshtastic_pygui-0.1.2.dist-info/METADATA'
adding 'meshtastic_pygui-0.1.2.dist-info/WHEEL'
adding 'meshtastic_pygui-0.1.2.dist-info/entry_points.txt'
adding 'meshtastic_pygui-0.1.2.dist-info/top_level.txt'
adding 'meshtastic_pygui-0.1.2.dist-info/RECORD'
removing build/bdist.linux-x86_64/wheel
Checking dist/meshtastic_pygui-0.1.2-py3-none-any.whl: PASSED
Checking dist/meshtastic_pygui-0.1.2.tar.gz: PASSED
Uploading distributions to https://test.pypi.org/legacy/
Enter your username: <yourpipyusername>
Enter your password: <yourpipypassword>
Uploading meshtastic_pygui-0.1.2-py3-none-any.whl
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 8.91k/8.91k [00:02<00:00, 4.09kB/s]
Uploading meshtastic_pygui-0.1.2.tar.gz
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7.43k/7.43k [00:01<00:00, 7.38kB/s]

View at:
https://test.pypi.org/project/meshtastic-pygui/0.1.2/
view the upload at https://test.pypi.org/ it it looks good upload for real
~/development/meshtastic/Meshtastic-PyGUI$
```

If that looks good, use 'bin/upload-release.sh' which works identically, but pushes the files to the production server.
