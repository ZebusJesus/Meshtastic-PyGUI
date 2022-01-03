# Note: you shouldn't need to run this script manually.  It is run implicitly by the pip3 install command.

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

with open("README.md", "r") as fh:
    long_description = fh.read()

# This call to setup() does all the work
setup(
    name="meshtastic_PyGUI",
    version="2.7.6",
    description="A pre-alpha python GUI for meshtastic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZebusJesus/Meshtastic-PyGUI",
    author="Zebus Jeus",
    author_email="ZebusJeus@pm.me",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["meshtastic_pygui"],
    include_package_data=True,
    install_requires=["meshtastic>=1.2.5", "PySimpleGUI>=4.34.0","requests>=2.25.1","esptool>=3.0"],
    extras_require={},
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "meshtastic_pygui=meshtastic_pygui.__main__:main",
        ]
    },
)
