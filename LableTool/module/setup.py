import cx_Freeze as cf
executables = [cf.Executable("/Users/kevinkuo/Documents/GitHub/LabelTool/LableTool/Label_Maker.py")]

cf.setup(
    name = "Label_Maker",
    options = {"build_exe" : {"packages":["tkinter","os","shutil","json","functools","PIL","zlib"],
                                "include_files":["/Users/kevinkuo/Documents/GitHub/LabelTool/LableTool/src/white.png"]}},
    executables = executables
)
