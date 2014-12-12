#!/usr/bin/env python

# numbertrack.py: main program loop
#
# Copyright (C) 2014 Jack Willis <jack@attac.us>
#
# This file is part of Numbertrack.
#
# Licensed under GNU General Public License 3.0 or later.
# Some rights reserved. See COPYING.

from tkinter import *
from tkinter.ttk import *

from numberstore import *

import webbrowser
import phonenumbers

NUMBERTRACK_VERSION = "0.0.1"

class NumberTrack(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.parent.title("Numbertrack v%s" % NUMBERTRACK_VERSION)

        self.numberstore = NumberStore("numbers.db")

        self.buildMenuBar()

        self.modifyEntry = Entry(self)
        self.modifyEntry.grid(row=0, column=0, columnspan=2, sticky=E+W)

        touchNumberButton = Button(self, text="Touch", command=self.touchNumber)
        touchNumberButton.grid(row=0, column=2, sticky=E+W)

        callNumberButton = Button(self, text="Call", command=self.callNumber)
        callNumberButton.grid(row=0, column=3, sticky=E+W)

        deleteNumberButton = Button(self, text="Delete", command=self.deleteNumber)
        deleteNumberButton.grid(row=0, column=4, sticky=E+W)

        self.numbersBox = Listbox(self)
        self.numbersBox.grid(row=1, column=0, columnspan=2, sticky=N+S+E+W)
        self.numbersBox.bind('<<ListboxSelect>>', self.selectNumber)

        fakeNumberList = ['+1 (555) 555-5551','+15555551212','212-2231','123-5678','727-8383','339-4422']
        for num in fakeNumberList:
            self.numberstore.touchNumber(num)

        for num in self.numberstore.getNumbers():
            self.numbersBox.insert(END, num)

        self.infoText = Text(self, width=10)
        self.infoText.grid(row=1, column=2, columnspan=3, sticky=N+S+E+W)

        self.showAllButton = Button(self, text="Show All", command=self.showAll)
        self.showAllButton.grid(row=2, column=0, sticky=E+W)

        self.searchButton = Button(self, text="Search", command=self.search)
        self.searchButton.grid(row=2, column=1, sticky=E+W)

        self.searchEntry = Entry(self)
        self.searchEntry.grid(row=2, column=2, columnspan=3, sticky=E+W)

        self.pack()

    def buildMenuBar(self):
        self.menu = Menu(self.parent)
        self.parent.config(menu=self.menu)

        self.fileMenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="New")
        self.fileMenu.add_command(label="Open")
        self.fileMenu.add_command(label="Save")

        self.editMenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.editMenu)
        self.editMenu.add_command(label="Locale")

        self.helpMenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.helpMenu)
        self.helpMenu.add_command(label="Documentation")
        self.helpMenu.add_command(label="About")

    def touchNumber(self):
        number = self.modifyEntry.get()
        self.numberstore.touchNumber(number)

    def callNumber(self):
        number = self.numbersBox.get(self.numbersBox.curselection())

        if not number.strip():
            return None

        print("calling number %s..." % number)

        formattedNumber = phonenumbers.format_number(phonenumbers.parse(number, "US"), phonenumbers.PhoneNumberFormat.E164)
        webbrowser.open("tel:%s" % formattedNumber)

    def saveInfo(self):
        number = self.modifyEntry.get()
        info = self.infoText.get('1.0', END)
        self.numberstore.setInfo(number, info.strip())

        print("set info of %s to %s" % (number, info))

    def deleteNumber(self):
        number = self.modifyEntry.get()
        self.numberstore.deleteNumber(number)

    # called when focus is called to an number in the listbox
    def selectNumber(self, evt):
        self.saveInfo()

        # get selected number
        w = evt.widget
        index = int(w.curselection()[0])
        number = w.get(index)

        # display the number in the top entry box
        self.modifyEntry.delete(0, END)
        self.modifyEntry.insert(0, number)

        # display the number's info in the text box
        info = self.numberstore.getInfo(number)
        self.infoText.delete("1.0", END)
        self.infoText.insert(END, (info or ""))

    def showAll(self, evt):
        print()

    def search(self, evt):
        print()

    def searchTags(self, evt):
        print()

def main():
    root = Tk()
    app = NumberTrack(root)
    root.mainloop()

if __name__ == '__main__':
    main()
