import cx_Freeze as cf
import os
import sys
base = None
if sys.platform == "win32":
    base = "Win32GUI"
executables = [cf.Executable("C:\\Users\\KevinBear\\Desktop\\LabelTool-master\\LableTool\\Label_Maker.py",base=base)]
os.environ['TCL_LIBRARY'] = r'C:\ProgramData\Anaconda3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\ProgramData\Anaconda3\tcl\tk8.6'
cf.setup(
    name = "Label_Maker",
    options = {"build_exe" : {"packages":["tkinter","os","shutil","json","functools","PIL","zlib"],
                                "include_files":["C:\\Users\\KevinBear\\Desktop\\LabelTool-master\\LableTool\\src\\"]}},
    executables = executables,
    version="1.0.0"
)