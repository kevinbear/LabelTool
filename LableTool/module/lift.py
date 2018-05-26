# import tkinter as tk
#
#
# ########################################################################
# class OtherFrame(tk.Toplevel):
#     """"""
#
#     #----------------------------------------------------------------------
#     def __init__(self):
#         """Constructor"""
#         tk.Toplevel.__init__(self)
#         self.geometry("400x300")
#         self.title("otherFrame")
#
# ########################################################################
# class MyApp(object):
#     """"""
#
#     #----------------------------------------------------------------------
#     def __init__(self, parent):
#         """Constructor"""
#         self.root = parent
#         self.root.title("Main frame")
#         self.frame = tk.Frame(parent)
#         self.frame.pack()
#
#         btn = tk.Button(self.frame, text="Open Frame", command=self.openFrame)
#         btn.pack()
#
#     #----------------------------------------------------------------------
#     def hide(self):
#         """"""
#         self.root.withdraw()
#
#     #----------------------------------------------------------------------
#     def openFrame(self):
#         """"""
#         self.hide()
#         subFrame = OtherFrame()
#         handler = lambda: self.onCloseOtherFrame(subFrame)
#         btn = tk.Button(subFrame, text="Close", command=handler)
#         btn.pack()
#
#     #----------------------------------------------------------------------
#     def onCloseOtherFrame(self, otherFrame):
#         """"""
#         otherFrame.destroy()
#         self.show()
#
#     #----------------------------------------------------------------------
#     def show(self):
#         """"""
#         #self.root.update()
#         self.root.deiconify()
#
#
# #----------------------------------------------------------------------
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.geometry("800x600")
#     app = MyApp(root)
#     root.mainloop()

import tkinter as tk

class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, height=42, width=42)
        self.entry = tk.Entry(self)
        self.entry.focus()
        self.entry.pack()
        self.clear_button = tk.Button(self, text="Clear text", command=self.clear_text)
        self.clear_button.pack()

    def clear_text(self):
        self.entry.delete(0, 'end')

def main():
    root = tk.Tk()
    App(root).pack(expand=True, fill='both')
    root.mainloop()

if __name__ == "__main__":
    main()
