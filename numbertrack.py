#!/usr/bin/env python

# numbertrack: store and keep track of phone numbers called
#
# Copyright (C) 2014 Jack Willis <jack@attac.us>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tkinter import *
from tkinter.ttk import *

import shelve
import datetime

import phonenumbers

NUMBERTRACK_VERSION = "0.0.1"

class NumberTrack(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.parent.title("Numbertrack v%s" % NUMBERTRACK_VERSION)

        self.numberstore = NumberStore("numbers.db")

        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(1, weight=1)

        self.modifyEntry = Entry(self)
        self.modifyEntry.grid(row=0, column=0, columnspan=2, sticky=E+W)
        self.modifyEntry.insert(0, "555-1212")

        touchNumberButton = Button(self, text="Touch", command=self.touchNumber)
        touchNumberButton.grid(row=0, column=2, sticky=E+W)

        touchNumberButton = Button(self, text="Update", command=self.updateInfo)
        touchNumberButton.grid(row=0, column=3, sticky=E+W)

        deleteNumberButton = Button(self, text="Delete", command=self.deleteNumber)
        deleteNumberButton.grid(row=0, column=4, sticky=E+W)

        self.numbersBox = Listbox(self)
        self.numbersBox.grid(row=1, column=0, columnspan=2, sticky=N+S+E+W)

        fakeNumberList = ['555-5551','212-2231','123-5678','727-8383','339-4422']

        for num in fakeNumberList:
            self.numbersBox.insert(END, num)

        self.infoText = Text(self)
        self.infoText.grid(row=1, column=2, columnspan=3, sticky=N+S+E+W)

        self.showAllButton = Button(self, text="Show All", command=self.showAll)
        self.showAllButton.grid(row=2, column=0, sticky=E+W)

        self.searchButton = Button(self, text="Search", command=self.search)
        self.searchButton.grid(row=2, column=1, sticky=E+W)

        self.searchEntry = Entry(self)
        self.searchEntry.grid(row=2, column=2, columnspan=3, sticky=E+W)


        self.pack()

    def touchNumber(self):
        number = self.modifyEntry.get()
        self.numberstore.touchNumber(number)

    def updateInfo(self):
        number = self.modifyEntry.get()
        info = self.infoText.get('1.0', END)
        self.numberstore.updateInfo(number, info)

    def deleteNumber(self):
        number = self.modifyEntry.get()
        self.numberstore.deleteNumber(number)

    def showAll(self):
        print()

    def search(self):
        print()

    def searchTags(self):
        print()

class NumberStore():
    def __init__(self, filename):
        self.db = shelve.open(filename, writeback=True)

        if not 'numbers' in self.db:
            self.db['numbers'] = {}

    def initNumber(self, number):
        if not number in self.db['numbers']:
            self.db['numbers'][number] = {'accesses': []}

    def touchNumber(self, number):
        self.initNumber(number)
        self.db['numbers'][number]['accesses'].append(datetime.datetime.now())

        print(self.db.__dict__['cache'])

    def updateInfo(self, number, info):
        self.initNumber(number)
        self.db['numbers'][number]['info'] = info

        print(self.db.__dict__['cache'])

    def deleteNumber(self, number):
        if number in self.db['numbers']:
            del self.db['numbers'][number]

        print(self.db.__dict__['cache'])

    def close(self):
        db.close()

def main():
    root = Tk()
    app = NumberTrack(root)
    root.mainloop()

if __name__ == '__main__':
    main()
