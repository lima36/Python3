# -*- coding: utf-8 -*-
import tkinter.messagebox
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog

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

    # def myfileOpen(self):
    #     self.myfile = tk.filedialog.askopenfile(filetypes=mypatterns, title='Open a Python file', mode='rb')
    #     loadedfile = self.myfile.read()
    #     self.myfile.close()
    #     print(loadedfile)

    def myfileOpen(self):
        self.myfile = tk.filedialog.askopenfile(filetypes=mypatterns, title='Open a Log file', mode='r')
        self.loadedfile = self.myfile.read()
        self.myfile.close()
        self.textView.insert("end", self.loadedfile)


    def filterWithKeyword(self):
        self.textView.delete("1.0", tk.END)
        # self.textView.insert("end", self.loadedfile)

    def myfilter(self):
        self.label = tk.Label(self.master, text="Keyword:")
        self.filter = tk.Entry(self.master, width=40)
        self.show = tk.Button(self.master, text="Filter", command=self.filterWithKeyword)

        self.label.pack(side='left', anchor='c')
        self.filter.pack(side='left')
        self.show.pack(side='left')


    def myNoteBook(self):
        self.notebook = ttk.Notebook(self.master, width=500, height=600)
        self.framenotebook1 = ttk.Frame(self.notebook)
        self.framenotebook2 = ttk.Frame(self.notebook)

        self.notebook.add(self.framenotebook1, text='Log')
        self.notebook.add(self.framenotebook2, text='Two')
        self.notebook.pack(side='top', expand='yes', fill='both')

        self.scrollbarView = tk.Scrollbar(self.framenotebook1,
                                          orient='vertical', takefocus=False, highlightthickness=0)
        self.scrollbarView_h = tk.Scrollbar(self.framenotebook1,
                                            orient='horizontal', takefocus=False, highlightthickness=0)

        self.textView = tk.Text(self.framenotebook1, bg='blue', fg='white', wrap='none', highlightthickness=0) #wrap='word'

        self.scrollbarView.config(command=self.textView.yview)
        self.scrollbarView_h.config(command=self.textView.xview)
        self.textView.config(yscrollcommand=self.scrollbarView.set)
        self.textView.config(xscrollcommand=self.scrollbarView_h.set)
        self.scrollbarView.pack(side='right', fill='y')
        self.scrollbarView_h.pack(side='bottom', fill='x')
        self.textView.pack(side='left', expand='yes', fill='both')

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

        aboutmenu = tk.Menu(mymenubar, tearoff=0)
        aboutmenu.add_command(label='Help', underline=0, accelerator='F1')
        aboutmenu.add_command(label='About IDLE-Plus', underline=0)
        mymenubar.add_cascade(label='Help', underline=0, menu=aboutmenu)

        self.master.configure(menu=mymenubar)


    def idleplusQuit(self, event=None):
        if tk.messagebox.askokcancel('Quit', 'Do you really want to exit?', parent=self.master):
            self.master.destroy()


window = tk.Tk()
myapp = IdlePlus(window)
window.mainloop()
