# -*- coding: utf-8 -*-
import tkinter.messagebox
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog
import utils
import logparse

myfonts = {'times': 'times 18 bold', 'verdana': 'Verdana 10'}
mypatterns = [('Logfile', '*.log'), ('Textfile', '*.txt')]


class IdlePlus(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent, class_='IdlePlus')
        self.myfile = None
        self.master = parent
        self.master.title('IDLE Plus')
        # self.master.geometry('500x500+250+50')
        self.master.geometry('1000x800+250+50')
        self.master.configure(bg='orange')
        self.master.bind('<Control-q>', self.idleplusQuit)
        self.master.bind('<Control-o>', self.myfileOpen)
        self.myBarMenu()
        self.myNoteBook()
        self.myfilter()

        self.bind('<Control-c>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-v>', self.paste)

    # def myfileOpen(self):
    #     self.myfile = tk.filedialog.askopenfile(filetypes=mypatterns, title='Open a Python file', mode='rb')
    #     loadedfile = self.myfile.read()
    #     self.myfile.close()
    #     print(loadedfile)

    def myfileOpen(self):
        self.myfile = tk.filedialog.askopenfile(filetypes=mypatterns, title='Open a Log file', mode='r')
        self.loadedfile = self.myfile.read()#.splitlines()
        self.myfile.close()
        self.textView.insert("end", self.loadedfile)


    def filterWithKeywordWithFile(self):
        self.textView.delete("1.0", tk.END)
        # self.textView.insert("end", self.loadedfile)
        print(self.myfile.name)
        print(self.filter.get())
        parsed = logparse.filterInLogfile(self.myfile.name, self.filter.get())
        self.textView.insert("end", parsed)


    def filterWithKeyword(self):
        self.textView.delete("1.0", tk.END)
        lines = [line for line in self.loadedfile.splitlines()]
        parsed = logparse.filterInList(lines, self.filter.get())
        for txt in parsed:
            self.textView.insert("end", txt+"\n")


    def myfilter(self):
        self.label = tk.Label(self.master, text="Keyword:")
        self.filter = tk.Entry(self.master, width=40)
        self.show = tk.Button(self.master, text="Filter", command=self.filterWithKeyword)
        self.test = tk.Button(self.master, text="Test", command=self.popupFileList)

        self.label.pack(side='left', anchor='c')
        self.filter.pack(side='left')
        self.show.pack(side='left')
        self.test.pack(side='right')

    def popupFileList(self):
        # if tk.messagebox.askokcancel('Quit', 'Do you really want to exit?', parent=self.master):
        information = utils.listAllFile(".", ".py")
        if tk.messagebox.showinfo("FileList", information):
            self.master.destroy()

    def myNoteBook(self):
        self.notebook = ttk.Notebook(self.master, width=500, height=600)
        self.framenotebook1 = ttk.Frame(self.notebook)
        self.framenotebook2 = ttk.Frame(self.notebook)
        self.framenotebook3 = ttk.Frame(self.notebook)

        self.notebook.add(self.framenotebook1, text='Log Analysis')
        self.notebook.add(self.framenotebook2, text='Robot Operation')
        self.notebook.add(self.framenotebook3, text='Elevator')
        self.notebook.pack(side='top', expand='yes', fill='both')

        self.scrollbarView = tk.Scrollbar(self.framenotebook1, orient='vertical', takefocus=False, highlightthickness=0)
        self.scrollbarView_h = tk.Scrollbar(self.framenotebook1, orient='horizontal', takefocus=False, highlightthickness=0)
        self.textView = tk.Text(self.framenotebook1, bg='blue', fg='white', wrap='none', highlightthickness=0) #wrap='word'
        self.scrollbarView.config(command=self.textView.yview)
        self.scrollbarView_h.config(command=self.textView.xview)
        self.textView.config(yscrollcommand=self.scrollbarView.set)
        self.textView.config(xscrollcommand=self.scrollbarView_h.set)
        self.scrollbarView.pack(side='right', fill='y')
        self.scrollbarView_h.pack(side='bottom', fill='x')
        self.textView.pack(side='left', expand='yes', fill='both')
        self.textView.bind("<Button-3><ButtonRelease-3>", self.do_popup)

        self.scrollbarView2 = tk.Scrollbar(self.framenotebook2, orient='vertical', takefocus=False, highlightthickness=0)
        self.scrollbarView_h2 = tk.Scrollbar(self.framenotebook2, orient='horizontal', takefocus=False, highlightthickness=0)
        self.textView2 = tk.Text(self.framenotebook2, bg='orange', fg='white', wrap='none', highlightthickness=0)  # wrap='word'
        self.scrollbarView2.config(command=self.textView2.yview)
        self.scrollbarView_h2.config(command=self.textView2.xview)
        self.textView2.config(yscrollcommand=self.scrollbarView2.set)
        self.textView2.config(xscrollcommand=self.scrollbarView_h2.set)
        self.scrollbarView2.pack(side='right', fill='y')
        self.scrollbarView_h2.pack(side='bottom', fill='x')
        self.textView2.pack(side='left', expand='yes', fill='both')

        self.scrollbarView3 = tk.Scrollbar(self.framenotebook3, orient='vertical', takefocus=False,
                                           highlightthickness=0)
        self.scrollbarView_h3 = tk.Scrollbar(self.framenotebook3, orient='horizontal', takefocus=False,
                                             highlightthickness=0)
        self.textView3 = tk.Text(self.framenotebook3, bg='green', fg='white', wrap='none',
                                 highlightthickness=0)  # wrap='word'
        self.scrollbarView3.config(command=self.textView3.yview)
        self.scrollbarView_h3.config(command=self.textView3.xview)
        self.textView3.config(yscrollcommand=self.scrollbarView3.set)
        self.textView3.config(xscrollcommand=self.scrollbarView_h3.set)
        self.scrollbarView3.pack(side='right', fill='y')
        self.scrollbarView_h3.pack(side='bottom', fill='x')
        self.textView3.pack(side='left', expand='yes', fill='both')


    def do_popup(self, event):
        m = tk.Menu(self.master, tearoff=0)
        m.add_command(label="Cut")
        m.add_command(label="Copy")
        m.add_command(label="Paste")
        m.add_command(label="Reload")
        m.add_separator()
        m.add_command(label="Exit")
        try:
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()

    def copy(self, event=None):
        self.clipboard_clear()
        text = self.get("sel.first", "sel.last")
        self.clipboard_append(text)
        print(text)

    def cut(self, event):
        self.copy()
        self.delete("sel.first", "sel.last")

    def paste(self, event):
        text = self.selection_get(selection='CLIPBOARD')
        self.insert('insert', text)

    def myBarMenu(self):
        mymenubar = tk.Menu(self.master)

        filemenu = tk.Menu(mymenubar, tearoff=0)
        filemenu.add_command(label='New File', underline=0, accelerator='CTRL+N')
        filemenu.add_command(label='Open File', underline=0, accelerator='CTRL+O', command=self.myfileOpen)
        filemenu.add_separator()
        filemenu.add_command(label='Save File', underline=0,accelerator='CTRL+S')
        filemenu.add_command(label='Save As...', accelerator='CTRL+SHIFT+S')
        filemenu.add_command(label='Close File', underline=0, accelerator='ALT+F4')
        filemenu.add_separator()
        filemenu.add_command(label='Print File', underline=0, accelerator='CTRL+P')
        filemenu.add_separator()
        filemenu.add_command(label='Exit', underline=0, accelerator='CTRL+Q', command=self.idleplusQuit)
        mymenubar.add_cascade(label='File', underline=0, menu=filemenu)
        filemenu.add_separator()
        filemenu.add_command(label='Log Info', underline=0, accelerator='CTRL+I', command=self.parseLogInfo)

        filemenu.add_separator()
        filemenu.add_command(label='Elevator', underline=0, accelerator='CTRL+L', command=self.parseElevator)


        aboutmenu = tk.Menu(mymenubar, tearoff=0)
        aboutmenu.add_command(label='Help', underline=0, accelerator='F1')
        aboutmenu.add_command(label='About IDLE-Plus', underline=0)
        mymenubar.add_cascade(label='Help', underline=0, menu=aboutmenu)

        self.master.configure(menu=mymenubar)


    def idleplusQuit(self, event=None):
        if tk.messagebox.askokcancel('Quit', 'Do you really want to exit?', parent=self.master):
            self.master.destroy()

    def parseLogInfo(self):
        self.myFoler_selected = tk.filedialog.askdirectory(parent=self.master, initialdir=".", title='Open a Log folder')
        files = utils.listdir(self.myFoler_selected)
        print(files)

        self.textView2.delete("1.0", tk.END)

        for f in files:
            print(f)
            self.textView2.insert("end", f)
            info = logparse.analysis_robot(f)
            self.textView2.insert("end", info)

    def parseElevator(self):
        self.myFoler_selected = tk.filedialog.askdirectory(parent=self.master, initialdir=".",
                                                           title='Open a Log folder')
        files = utils.listdir(self.myFoler_selected)
        print(files)

        self.textView3.delete("1.0", tk.END)

        for f in files:
            print(f)
            self.textView3.insert("end", f)
            info = logparse.analysis_elevator(f)
            self.textView3.insert("end", info)
        pass


window = tk.Tk()
myapp = IdlePlus(window)
window.mainloop()
