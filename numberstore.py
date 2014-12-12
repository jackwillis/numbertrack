# numberstore.py: manage phone number database
#
# Copyright (C) 2014 Jack Willis <jack@attac.us>
#
# This file is part of Numbertrack.
#
# Licensed under GNU General Public License 3.0 or later.
# Some rights reserved. See COPYING.

import shelve
import datetime

class NumberStore():
    def __init__(self, filename):
        self.db = shelve.open(filename, writeback=True)

        if not 'numbers' in self.db:
            self.db['numbers'] = {}

    def initNumber(self, number):
        if not number in self.db['numbers']:
            self.db['numbers'][number] = {'accesses': [], 'info': '#yolo'}

    def touchNumber(self, number):
        self.initNumber(number)
        self.db['numbers'][number]['accesses'].append(datetime.datetime.now())

        print(self.db.__dict__['cache'])

    def getNumbers(self):
        return self.db['numbers']

    def getAccesses(self, number):
        if not number in self.db['numbers']:
            return None
        if not 'info' in self.db['numbers'][number]:
            return None

        return self.db['numbers'][number]['info']

    def getInfo(self, number):
        if not number in self.db['numbers']:
            return None

        return self.db['numbers'][number]['info']

    def setInfo(self, number, info):
        self.initNumber(number)
        self.db['numbers'][number]['info'] = info

        print(self.db.__dict__['cache'])

    def deleteNumber(self, number):
        if number in self.db['numbers']:
            del self.db['numbers'][number]

        print(self.db.__dict__['cache'])

    def close(self):
        db.close()
