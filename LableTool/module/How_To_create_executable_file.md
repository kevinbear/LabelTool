# Create Lable_Maker executable binary file

1. Window 10 
- 安裝套件 cx_Freeze
  + `pip install cx_Freeze`
- 更改 Win_setup.py 的程式碼 把以下三行的路徑改成使用者自電腦內的路徑
  + C:\\Users\\KevinBear\\Desktop\\LabelTool-master\\LableTool\\Label_Maker.py --> Modify user computer Label_Maker.py path
  + r'C:\ProgramData\Anaconda3\tcl\tcl8.6' --> Modify to user computer anaconda tcl tcl8.6 path
  + r'C:\ProgramData\Anaconda3\tcl\tk8.6' --> Modify to user computer anaconda tcl tk8.6 path
  ```
  executables = [cf.Executable("C:\\Users\\KevinBear\\Desktop\\LabelTool-master\\LableTool\\Label_Maker.py",base=base)]
  os.environ['TCL_LIBRARY'] = r'C:\ProgramData\Anaconda3\tcl\tcl8.6'
  os.environ['TK_LIBRARY'] = r'C:\ProgramData\Anaconda3\tcl\tk8.6'
  ```
- cmd run `python Win_setup.py bdist_msi`
- 運行完 Win_setup.py 後，至資料夾內可以看到build、dist兩個檔案
  + build --> 內有執行檔
  + dist --> 內有安裝檔
2. Mac OS (High sierra 10.13)
- 安裝套件 cx_Freeze
  + `pip install cx_Freeze`
- Terminal run `python setup.py build`
- 運行完 setup.py 後，至資料夾內可以看到build一個檔案
  + build --> 內有執行檔(點擊安裝檔後會報錯)
