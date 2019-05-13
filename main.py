# -*- coding:utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.constants import *
from tkinter.filedialog import asksaveasfilename
from win32gui import GetForegroundWindow, GetWindowText, GetWindowRect, FindWindow, SetForegroundWindow
from tkinter.messagebox import showerror
APP_NAME = "MapleMemo"
APP_NAME_SAVE = "저장할 경로 선택 - MapleMemo"

class MainFrame(tk.Frame):
    """
    This class is just a Toplevel window.
    """

    def __init__(self, parent):
        super(MainFrame, self).__init__(parent)
        self.parent = parent
        self.pack(expand=YES, fill=BOTH)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=YES, fill=BOTH)

        self.text_frame = tk.Frame(self.notebook)
        self.text = ScrolledText(self.text_frame)
        self.text.pack(expand=YES, fill=BOTH)

        self.checkbox_frame = tk.Frame(self.notebook)
        self.checkbox_frame.grid_columnconfigure(0, weight=1)
        for x in range(10):

            tk.Entry(self.checkbox_frame, borderwidth=1, relief=SOLID).grid(row=x, column=0, sticky=E+W, pady=5, padx=(5,0))
            tk.Checkbutton(self.checkbox_frame).grid(row=x, column=1, sticky=E+W, pady=5, padx=(0,5))

        self.notebook.add(self.text_frame, text="메모장")
        self.notebook.add(self.checkbox_frame, text="체크박스")

        self.option_frame = tk.Frame(self)
        self.option_frame.pack(side=BOTTOM, fill=X)

        self.grip = ttk.Sizegrip(self.option_frame)
        self.grip.pack(side=RIGHT)
        self.grip.bind("<B1-Motion>", self.OnMotion)
        self.grip.bind("<ButtonRelease-1>", self.OnMotionRelease)
        tk.Label(self.option_frame, text="Dashadower").pack(side=RIGHT)
        tk.Button(self.option_frame, text="종료", command=self.onExit).pack(side=LEFT)
        tk.Button(self.option_frame, text="파일로 저장하기", command=self.onSave).pack(side=LEFT)
        tk.Button(self.option_frame, text="위치 바꾸기", command=self.onRelocate).pack(side=LEFT)

        self.last_window_name = None
        self.window_location = "right"

        SetForegroundWindow(FindWindow(0, "MapleStory"))
        self.after(1, self.tick)

    def onRelocate(self):
        self.window_location = "right" if self.window_location == "left" else "left"
        if self.window_location == "right":
            _, cy, cx, _ = GetWindowRect(FindWindow(0, "MapleStory"))
            root.geometry("+%d+%d" % (cx, cy))
        else:
            cx, cy, _, _ = GetWindowRect(FindWindow(0, "MapleStory"))
            root.geometry("+%d+%d" % (cx - root.winfo_width(), cy))


    def onExit(self):
        root.destroy()

    def onSave(self):
        save_path = asksaveasfilename(title=APP_NAME_SAVE, filetypes=[("텍스트 파일(*.txt)", "*.txt"), ("모든 파일", "*.*")], defaultextension=".txt")
        if not save_path: return
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(self.text.get("1.0", END))


    def OnMotion(self, event):
        x1 = self.winfo_pointerx()
        y1 = self.winfo_pointery()
        x0 = self.winfo_rootx()
        y0 = self.winfo_rooty()
        root.geometry("%sx%s" % ((x1 - x0), (y1 - y0)))

        return

    def OnMotionRelease(self, event):
        if self.window_location == "right":
            _, cy, cx, _ = GetWindowRect(FindWindow(0, "MapleStory"))
            root.geometry("+%d+%d" % (cx, cy))
        else:
            cx, cy, _, _ = GetWindowRect(FindWindow(0, "MapleStory"))
            root.geometry("+%d+%d" % (cx - root.winfo_width(), cy))

    def tick(self):
        cwindow = GetForegroundWindow()
        foreground_window_text = GetWindowText(cwindow)
        if foreground_window_text == "MapleStory" and foreground_window_text != APP_NAME_SAVE:

            if self.window_location == "right":
                _, cy, cx, _ = GetWindowRect(FindWindow(0, "MapleStory"))
                root.geometry("+%d+%d"%(cx, cy))
            else:
                cx, cy, _, _ = GetWindowRect(FindWindow(0, "MapleStory"))
                root.geometry("+%d+%d" % (cx-root.winfo_width(), cy))
            root.attributes("-topmost", True)
            root.lift()
        elif foreground_window_text == APP_NAME_SAVE:
            root.attributes("-topmost", False)
            root.attributes("-topmost", None)
        elif foreground_window_text != APP_NAME:
            root.attributes("-topmost", False)
            root.attributes("-topmost", None)
            root.lower()
        root.update()
        root.update_idletasks()
        self.last_window_name = foreground_window_text
        self.after(10, self.tick)








if __name__ == '__main__':
    root = tk.Tk()
    root.title(APP_NAME)
    root.overrideredirect(True)
    root.wm_minsize(300, 350)
    if not FindWindow(0, "MapleStory"):
        root.withdraw()
        showerror(APP_NAME, "메이플스토리 창을 찾지 못했습니다..")
        root.destroy()
    else:
        MainFrame(root)
    root.mainloop()

