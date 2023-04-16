from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import ttk
import requests
import time
import json
from googletrans import Translator, constants
from pprint import pprint
#from Globals import *
from Globals import *

class TextEditor:

    def __init__(self):
        """Class initialization."""
        self.translator = Translator()
        self.root = Tk()
        self.root.title(app_name)
        self.root.geometry(dimen)
        self.root.configure(bg=grey_color)

        global open_status_name
        self.open_status_name = False

    def new_file(self):
        """Creation of a new file."""
        self.my_text.delete("1.0", END)
        self.root.title(new_file_label)
        self.status_bar.config(text=new_file_status)

        global open_status_name
        self.open_status_name = False

    def open_file(self):
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

    def save_as_file(self):
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

    def save_file(self):
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

    def get_text(self):
        """Translation of a word or a phrase."""
        try:
            self.text_to_translate = self.my_text.selection_get()
            self.result = self.translator.translate(
                self.text_to_translate, src=eng, dest=rus).text
            self.translation_bar.config(text=self.result)
        except BaseException:
            pass

    def init_frame(self):
        """Main frame initialization."""
        self.my_frame = Frame(self.root)
        self.my_frame.pack(pady=padd)

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

    def init_translation_btn(self):
        """Initialization of the translation button."""
        self.button = ttk.Button(text=translate_label, command=self.get_text)
        self.button.pack(side=BOTTOM)

    def init_file_menu(self):
        """Initialization of all possible menu functions."""
        self.file_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label=menu_file, menu=self.file_menu)
        self.file_menu.add_command(label=menu_new, command=self.new_file)
        self.file_menu.add_command(label=menu_open, command=self.open_file)
        self.file_menu.add_command(label=menu_save, command=self.save_file)
        self.file_menu.add_command(
            label=menu_save_as,
            command=self.save_as_file)

    def set_dependencies(self):
        """Setting up translation and status bars."""
        self.translation_bar = Label(
            self.root, text=translate_status, anchor=W)
        self.status_bar = Label(self.root, text=ready_label, anchor=E)
        self.status_bar.pack(fill=X, side=BOTTOM, ipady=padd)
        self.translation_bar.pack(fill=X, side=BOTTOM, ipady=padd)
        self.translation_bar.configure(anchor=an)

    def set_up(self):
        """Calling init functions in the right order."""
        self.init_frame()
        self.init_scroll()
        self.init_text()
        self.init_menu()
        self.init_translation_btn()
        self.init_file_menu()
        self.set_dependencies()
        self.root.mainloop()
