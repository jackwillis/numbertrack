# numberstore.py: manage phone number database
#
# Copyright (C) 2014 Jack Willis <jack@attac.us>
#
# This file is part of Numbertrack.
#
# Licensed under GNU General Public License 3.0 or later.
# Some rights reserved. See COPYING.

from tinydb import TinyDB, where
import datetime

class NumberStore():
    def __init__(self, filename):
        self.db = TinyDB(filename)

    def initNumber(self, number):
        if not self.getNumberDict(number):
            self.db.insert({'number': number, 'accesses': [], 'info': '#yolo'})

    def touchNumber(self, number):
        self.initNumber(number)

        #print(self.getNumberDict(number))
        #accesses = self.getNumberDict(number)['accesses'].append(datetime.datetime.now())

        #self.db.update({'accesses': accesses}, where('number') == number)

    def getNumberDict(self, number):
        return self.db.get(where('number') == number)

    def getNumberList(self):
        return (entry['number'] for entry in self.db.all())

    def getAccesses(self, number):
        # if not number in self.db['numbers']:
        #     return None
        # if not 'info' in self.db['numbers'][number]:
        #     return None
        #
        # return self.db['numbers'][number]['info']
        return []

    def getInfo(self, number):
        return self.getNumberDict(number)['info']

    def setInfo(self, number, info):
        self.initNumber(number)
        self.db.update({'info': info}, where('number') == number)

        print(self.db.all())

    def deleteNumber(self, number):
        self.db.remove(where('number') == number)

        print(self.db.all())

    def close(self):
        self.db.close()
