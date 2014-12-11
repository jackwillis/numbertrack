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

class NumberTrack(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.parent.title("numbertrack")

        self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="Add number", command=self.addNumber)
        quitButton.place(x=50, y=50)

    def addNumber(self):
        print("test")


def main():
    root = Tk()
    root.geometry("400x200")
    app = NumberTrack(root)
    root.mainloop()

if __name__ == '__main__':
    main()
