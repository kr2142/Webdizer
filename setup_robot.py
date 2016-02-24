import sys
from cx_Freeze import setup, Executable


build_exe_options = {"packages": ["BeautifulSoup", "os"], "includes": ["BeautifulSoup", "os","hashlib","re","urllib2", "datetime","Tkinter", "collections"]}
base = None


setup( name = "Webdizer",
version = "1.0",
description = "My GUI application!",
options = {"build_exe": build_exe_options},
executables = [Executable(script = "webdizer.py", icon ='grendizer.ico')])
