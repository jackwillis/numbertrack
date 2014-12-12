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
from tkinter.messagebox import *
from tkinter.filedialog import *
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

        self.parent.protocol("WM_DELETE_WINDOW", self.quit)

        self.numberstore = None

        self.buildMenuBar()
        self.buildModifyEntry()
        self.buildActionButtons()
        self.buildNumbersBox()
        self.buildInfoText()
        self.buildBottomRow()

        self.parent.bind('<Delete>', lambda evt: self.deleteNumber())

        #fakeNumberList = ['+1 (555) 555-5551','+15555551212','212-2231','123-5678','727-8383','339-4422']
        #for num in fakeNumberList:
        #    self.numberstore.touchNumber(num)

        self.pack()

    def buildMenuBar(self):
        self.menu = Menu(self.parent)
        self.parent.config(menu=self.menu)

        self.fileMenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="New")
        self.fileMenu.add_command(label="Open", command=self.openDialog)
        self.fileMenu.add_command(label="Save As")

        self.editMenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.editMenu)
        self.editMenu.add_command(label="Locale")

        self.helpMenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.helpMenu)
        self.helpMenu.add_command(label="Documentation")
        self.helpMenu.add_command(label="About", command=self.aboutDialog)

    def buildModifyEntry(self):
        self.modifyEntry = Entry(self)
        self.modifyEntry.grid(row=0, column=0, columnspan=2, sticky=E+W)

    def buildActionButtons(self):
        addNumberButton = Button(self, text="Add", command=self.addNumber)
        addNumberButton.grid(row=0, column=2, sticky=E+W)

        touchNumberButton = Button(self, text="Touch", command=self.touchNumber)
        touchNumberButton.grid(row=0, column=3, sticky=E+W)

        callNumberButton = Button(self, text="Call", command=self.callNumber)
        callNumberButton.grid(row=0, column=4, sticky=E+W)

        deleteNumberButton = Button(self, text="Delete", command=self.deleteNumber)
        deleteNumberButton.grid(row=0, column=5, sticky=E+W)

    def buildNumbersBox(self):
        self.numbersBox = Listbox(self)
        self.numbersBox.grid(row=1, column=0, columnspan=2, sticky=N+S+E+W)
        self.numbersBox.bind('<<ListboxSelect>>', lambda evt: self.selectNumber())

    def populateNumbersBox(self):
        for num in self.numberstore.getNumberList():
            if num:
                self.numbersBox.insert(END, num)

    def buildInfoText(self):
        self.infoText = Text(self, width=10)
        self.infoText.grid(row=1, column=2, columnspan=4, sticky=N+S+E+W)

    def buildBottomRow(self):
        self.showAllButton = Button(self, text="Show All", command=self.showAll)
        self.showAllButton.grid(row=2, column=0, sticky=E+W)

        self.searchButton = Button(self, text="Search", command=self.search)
        self.searchButton.grid(row=2, column=1, sticky=E+W)

        self.searchEntry = Entry(self)
        self.searchEntry.grid(row=2, column=2, columnspan=4, sticky=E+W)

    def refresh(self):
        number = self.modifyEntry.get()
        info = self.numberstore.getInfo(number)

        self.infoText.delete("1.0", END)
        self.infoText.insert(END, (info or ""))

    def addNumber(self):
        number = self.modifyEntry.get().strip()

        if not number:
            return None

        self.numberstore.initNumber(number)

        self.numbersBox.insert(0, number)
        self.numbersBox.selection_set(0, 0)

    def touchNumber(self):
        number = self.modifyEntry.get()
        self.numberstore.touchNumber(number)

    def callNumber(self):
        number = self.modifyEntry.get()

        if not number.strip():
            return None

        formattedNumber = phonenumbers.format_number(phonenumbers.parse(number, "US"), phonenumbers.PhoneNumberFormat.E164)
        webbrowser.open("tel:%s" % formattedNumber)

        print(formattedNumber)

    def saveInfo(self):
        number = self.modifyEntry.get()
        info = self.infoText.get('1.0', END)
        self.numberstore.setInfo(number, info.strip())

        print("set info of %s to %s" % (number, info))

    def deleteNumber(self):
        number = self.modifyEntry.get()
        self.numberstore.deleteNumber(number)

        selection = self.numbersBox.curselection()
        self.numbersBox.delete(selection)
        self.numbersBox.selection_set(selection, selection)
        self.numbersBox.focus()

        self.selectNumber()

    def selectNumber(self):
        self.saveInfo()

        index = int(self.numbersBox.curselection()[0])
        number = self.numbersBox.get(index)

        # display the number in the top entry box
        self.modifyEntry.delete(0, END)
        self.modifyEntry.insert(0, number)

        self.refresh()

    def showAll(self, evt):
        print()

    def search(self, evt):
        print()

    def searchTags(self, evt):
        print()

    def openDialog(self):
        filename = askopenfilename()
        self.numberstore = NumberStore(filename)

        self.populateNumbersBox()
        self.refresh()

    def aboutDialog(self):
        showinfo(title="About Numbertrack",
                 message="Numbertrack v%s. <http://www.attac.us/numbertrack/>\n" % NUMBERTRACK_VERSION +
                          "Licensed under GNU General Public License 3.0 or later.")

    def quit(self):
        if self.numberstore:
            self.numberstore.close()
        self.parent.quit()


def main():
    root = Tk()
    app = NumberTrack(root)
    root.mainloop()

if __name__ == '__main__':
    main()
