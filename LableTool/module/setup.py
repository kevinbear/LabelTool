#for mac os
import cx_Freeze as cf
executables = [cf.Executable("/Users/kevinkuo/Documents/GitHub/LabelTool/LableTool/Label_Maker.py")]

cf.setup(
    name = "Label_Maker",
    options = {"build_exe" : {"includes":["tkinter","os","shutil","json","functools","PIL"],
                                "include_files":["/Users/kevinkuo/Documents/GitHub/LabelTool/LableTool/src/"]}},
    executables = executables
)
