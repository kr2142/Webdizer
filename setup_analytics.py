import sys
from cx_Freeze import setup, Executable


build_exe_options = {"packages": ["guess_language" ], "includes": ["BeautifulSoup",
                                                                       "os","matplotlib.pyplot","random", "datetime","Tkinter",
                                                                       "collections", "guess_language","matplotlib.backends.backend_tkagg" ]}

setup( name = "Analyzer",
version = "1.0",
description = "My GUI application!",
options = {"build_exe": build_exe_options},
executables = [Executable(script = "analyzer.py", icon ='research.ico')])

#After building copy 'guess_language' directory to 'exe.win32-2.7'
