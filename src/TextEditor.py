from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import ttk
import requests
import time
import json
from pprint import pprint
from Globals import *

class TextEditor:

    def __init__(self):
        """Class initialization."""
        self.root = Tk()
        self.root.title(app_name)
        self.root.geometry(dimen)
        self.root.configure(bg=grey_color)

        global open_status_name
        self.open_status_name = False

    def new_file(self, event=None):
        """Creation of a new file."""
        self.my_text.delete("1.0", END)
        self.root.title(new_file_label)
        self.status_bar.config(text=new_file_status)

        global open_status_name
        self.open_status_name = False

    def open_file(self, event=None):
        """Opening a file in the editor window."""
        self.text_file = filedialog.askopenfilename(
            initialdir=initdir, title=open_file_label, filetypes=filetyp)
        if self.text_file:
            self.my_text.delete("1.0", END)
            global open_status_name
            self.open_status_name = self.text_file
            self.name = self.text_file
            self.status_bar.config(text=f'{self.name}        ')
            self.root.title(f'{self.name}')
            self.text_file = open(self.text_file, 'r')
            self.stuff = self.text_file.read()
            self.my_text.insert(END, self.stuff)
            self.text_file.close()

    def save_as_file(self, event=None):
        """Saving file as some extention."""
        self.text_file = filedialog.asksaveasfilename(
            defaultextension=".*",
            initialdir=initdir,
            title=save_file_label,
            filetypes=filetyp)
        if self.text_file:
            self.name = self.text_file
            global open_status_name
            self.open_status_name = self.text_file
            self.status_bar.config(text=f'Saved{self.name}        ')
            self.root.title(f'{self.name}')

            self.text_file = open(self.text_file, 'w')
            self.text_file.write(self.my_text.get(1.0, END))
            self.text_file.close()

    def save_file(self, event=None):
        """Saving file with set up name and extension if those exist."""
        global open_status_name
        if self.open_status_name:
            self.text_file = open(self.open_status_name, 'w')
            self.text_file.write(self.my_text.get(1.0, END))
            self.text_file.close()

            self.status_bar.config(
                text=f'Saved{self.open_status_name}        ')
        else:
            self.save_as_file()
            
    def quit_program(self, event=None):
        self.root.destroy()
        
    def end_line(self, event=None):
        lineidx = int(self.my_text.index(INSERT).split('.')[0]) - 1
        line = self.my_text.get(1.0, END).split('\n')[lineidx]
        endidx = len(line) - 1
        self.my_text.mark_set(insert_log, "%d.%d" % (lineidx + 1, endidx + 1))
        
    def begin_line(self, event=None):
        lineidx = int(self.my_text.index(INSERT).split('.')[0]) - 1
        endidx = -1
        self.my_text.mark_set(insert_log, "%d.%d" % (lineidx + 1, endidx + 1))
        
    def init_frame(self):
        """Main frame initialization."""
        self.my_frame = Frame(self.root)
        self.my_frame.pack(pady=padd)
        self.root.bind(cf, self.find)
        self.root.bind(cr, self.replace)
        self.root.bind(cn, self.new_file)
        self.root.bind(co, self.open_file)
        self.root.bind(cs, self.save_file)
        self.root.bind(cq, self.quit_program)
        self.root.bind(cj, self.end_line)
        self.root.bind(cg, self.begin_line)

    def init_scroll(self):
        """Text scroll initialization."""
        self.text_scroll = Scrollbar(self.my_frame)
        self.text_scroll.pack(side=RIGHT, fill=Y)

    def init_text(self):
        """Initialization of text editor window."""
        self.my_text = Text(
            self.my_frame,
            width=dimx,
            height=dimy,
            font=(
                chosen_font,
                font_size),
            selectbackground=pink_color,
            selectforeground=black_color,
            undo=True,
            yscrollcommand=self.text_scroll.set)
        self.my_text.pack()
        self.text_scroll.config(command=self.my_text.yview)

    def init_menu(self):
        """Menu line initialization."""
        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)

        
    def init_file_menu(self):
        """Initialization of all possible menu functions."""
        self.file_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label=menu_file, menu=self.file_menu)
        self.file_menu.add_command(label=menu_new, command=self.new_file, accelerator=ctn)
        self.file_menu.add_command(label=menu_open, command=self.open_file, accelerator=cto)
        self.file_menu.add_command(label=menu_save, command=self.save_file, accelerator=cts)
        self.file_menu.add_command(
            label=menu_save_as,
            command=self.save_as_file)
        self.edit_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label=edit_label, menu=self.edit_menu)
        self.edit_menu.add_command(label=find_label, command=self.find, accelerator=ctf)
        self.edit_menu.add_command(label=replace_label, command=self.replace, accelerator=ctr)

    def find_string(self, findString):
        """Finding the given string in the input text."""
        startInd = '1.0'
        while(startInd):
            startInd = self.my_text.search(findString, startInd, stopindex=END)
            if startInd:
                startInd = str(startInd)
                lastInd = startInd+f'+{len(findString)}c'
                print(startInd, lastInd)
                self.my_text.tag_add(highlight, startInd, lastInd)
                startInd = lastInd
                
    def replace(self, event=None):
        """Replacing the given string with another one in the input text."""
        tl = Toplevel(self.root)
        tl.title("Find and Replace")
        tl.transient(self.root)
        tl.focus_force()
        tl.grid_columnconfigure(0, weight=1)
        tl.grid_rowconfigure(0, weight=1)
        e1 = ttk.Entry(tl)
        e1.grid(row=0, column=0, pady=5, columnspan=3, padx=10)
        e2 = ttk.Entry(tl)
        e2.grid(row=1, column=0, pady=5, columnspan=3, padx=10)

        def find():
            findString = e1.get()
            self.set_mark(findString)

        def replace():
            findString = e1.get()
            replaceString = e2.get()
            myText = self.my_text.get('1.0', END)
            myText = myText.replace(findString, replaceString, 1)
            self.my_text.delete('1.0', END)
            self.my_text.insert('1.0', myText)

        def on_closing():
            self.my_text.tag_delete(highlight)
            tl.destroy()

        def replaceAll():
            findString = e1.get()
            replaceString = e2.get()
            myText = self.my_text.get('1.0', END)
            myText = myText.replace(findString, replaceString)
            self.my_text.delete('1.0', END)
            self.my_text.insert('1.0', myText)

        findButton = ttk.Button(tl, text=find_label, command=find)
        replaceButton = ttk.Button(tl, text=replace_label, command=replace)
        replaceAllButton = ttk.Button(tl, text=replace_all_label, command=replaceAll)
        findButton.grid(row=3, column=0, padx=10, pady=5)
        replaceButton.grid(row=3, column=1, padx=10, pady=5)
        replaceAllButton.grid(row=3, column=2, padx=10, pady=5)
        tl.protocol(on_del, on_closing)
        
    def set_mark(self, findString):
        """Making the highlighted text visible."""
        self.find_string(findString)
        self.my_text.tag_config(highlight, foreground=red_color)
        self.my_text.focus_force()
        
    def find(self, event=None):
        """Enabling the search of a substring in the input text."""
        tl = Toplevel(self.root)
        tl.title(find_label)
        tl.transient(self.root)
        tl.focus_force()
        tl.grid_columnconfigure(0, weight=1)
        tl.grid_rowconfigure(0, weight=1)
        e1 = ttk.Entry(tl)
        e1.grid(row=0, column=0, pady=pads,
                padx=pads, columnspan=2, sticky=ew)

        def sub():
            findString = e1.get()
            print(findString)
            self.set_mark(findString)

        def on_closing():
            self.my_text.tag_delete(highlight)
            tl.destroy()

        findBtn = ttk.Button(tl, text=find_label, command=sub)
        findBtn.grid(row=1, column=0, pady=pads, padx=pads, sticky=ews)
        closeBtn = ttk.Button(tl, text=close_label, command=on_closing)
        closeBtn.grid(row=1, column=1, pady=pads, padx=pads, sticky=ews)
        tl.protocol(on_del, on_closing)
        
    def set_dependencies(self):
        """Setting up status bars."""
        self.status_bar = Label(self.root, text=ready_label, anchor=E)
        self.status_bar.pack(fill=X, side=BOTTOM, ipady=padd)

    def set_up(self):
        """Calling init functions in the right order."""
        self.init_frame()
        self.init_scroll()
        self.init_text()
        self.init_menu()
        self.init_file_menu()
        self.set_dependencies()
        self.root.mainloop()
