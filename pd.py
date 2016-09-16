##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2013 Uwe Hermann <uwe@hermann-uwe.de>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
##

import sigrokdecode as srd

'''
OUTPUT_PYTHON format:

Packet:
[<ptype>, <pdata>]

<ptype>, <pdata>
 - 'ITEM', [<item>, <itembitsize>]
 - 'WORD', [<word>, <wordbitsize>, <worditemcount>]

<item>:
 - A single item (a number). It can be of arbitrary size. The max. number
   of bits in this item is specified in <itembitsize>.

<itembitsize>:
 - The size of an item (in bits). For GPIB 8 data + 8 control.

<sample_total>;
 - Total number of samples, needed to show the last byte

<debug>:
 - Flag to enable debug prints

2016-09-15, Rudolf Reuter, GPIB decoding of 16 bits,
            derived from decoder "parallel".
            Pins CLK, DAV, EOI, ATN must be set for proper decoding.

'''

class ChannelError(Exception):
    pass

class Decoder(srd.Decoder):
    api_version = 2
    id = 'gpib'
    name = 'gpib'
    longname = 'General Purpose Interface Bus'
    desc = 'GPIB, HPIB, IEEE488.'
    license = 'gplv2+'
    inputs = ['logic']
    outputs = ['gpib']

    # keyword "channels" does NOT work
    optional_channels = (
        {'id': 'clk', 'name': 'CLK', 'desc': 'Clock line'},
        {'id': 'd0' , 'name': 'D0', 'desc': 'Data line 0'},
        {'id': 'd1' , 'name': 'D1', 'desc': 'Data line 1'},
        {'id': 'd2' , 'name': 'D2', 'desc': 'Data line 2'},
        {'id': 'd3' , 'name': 'D3', 'desc': 'Data line 3'},
        {'id': 'd4' , 'name': 'D4', 'desc': 'Data line 4'},
        {'id': 'd5' , 'name': 'D5', 'desc': 'Data line 5'},
        {'id': 'd6' , 'name': 'D6', 'desc': 'Data line 6'},
        {'id': 'd7' , 'name': 'D7', 'desc': 'Data line 7'},
        {'id': 'EOI', 'name': 'EOI', 'desc': 'End Or Identify, 8'},
        {'id': 'DAV', 'name': 'DAV', 'desc': 'Clock, falling edge, 9'},
        {'id': 'NRFD', 'name': 'NRFD', 'desc': 'Not Ready For Data, 10'},
        {'id': 'NDAC', 'name': 'NDAC', 'desc': 'Not Data Accepted, 11'},
        {'id': 'IFC', 'name': 'IFC', 'desc': 'InerFace Clear, 12'},
        {'id': 'SRQ', 'name': 'SRQ', 'desc': 'Service ReQuest, 13'},
        {'id': 'ATN', 'name': 'ATN', 'desc': 'ATN,Command mode, 14'},
        {'id': 'REN', 'name': 'REN', 'desc': 'Remote ENable, 15'},
    )
    options = (
        {'id': 'sample_total', 'desc': 'total number of samples', 'default': 0},
        {'id': 'debug', 'desc': 'debug print',
            'default': 'False', 'values': ('False', 'True')},
    )
    annotations = (
        ('items', 'Items'),
         ('gpib', 'DAT/CMD'),
         ('eoi', 'EOI'),
    )
    annotation_rows = (
        ('items', 'Bytes', (0,)),
        ('gpib', 'DAT/CMD', (1,)),
        ('eoi', 'EOI', (2,)),
    )

    def __init__(self):
        self.oldclk = None
        self.items = []
        self.itemcount = 0
        self.saved_item = None
        self.saved_ATN = False
        self.saved_EOI = False
        self.samplenum = 0
        self.oldpins = None
        self.ss_item = self.es_item = None
        self.first = True
        self.last = False
        self.debug = False

    def start(self):
        strdebug = self.options['debug']
        if strdebug == 'True': self.debug = True
        if self.debug: print('start GPIB decoder')
        self.out_python = self.register(srd.OUTPUT_PYTHON)
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def putpb(self, data):
        self.put(self.ss_item, self.es_item, self.out_python, data)

    def putb(self, data):
        self.put(self.ss_item, self.es_item, self.out_ann, data)

    def handle_bits(self, datapins):
        dbyte = 0x20
        dATN = False
        item2 = False
        dEOI = False
        item3 = False
        # If this is the first item in a word, save its sample number.
        if self.itemcount == 0:
            self.ss_word = self.samplenum

        # Get the bits for this item.
        item, used_pins = 0, datapins.count(b'\x01') + datapins.count(b'\x00')
        for i in range(used_pins):
            item |= datapins[i] << i

        item = item & 0xff  # mask 8-bit data byte
        item = item ^ 0xff  # invert data byte
        #if self.debug: print('%02X' % item)
        self.items.append(item)
        self.itemcount += 1
        if datapins[14] == 0: item2 = True 
        if datapins[8] == 0: item3 = True

        if self.first:
            # Save the start sample and item for later (no output yet).
            self.ss_item = self.samplenum
            self.first = False
            self.saved_item = item
            self.saved_ATN = item2
            self.saved_EOI = item3

        else:
            # Output the saved item (from the last CLK edge to the current).
            dbyte = self.saved_item
            dATN = self.saved_ATN
            dEOI = self.saved_EOI
            self.es_item = self.samplenum
            #self.putpb(['ITEM', self.saved_item])    # to Python output
            self.putb([0, ['%02X' % self.saved_item]]) # to annotation row = 0

            # here encode item byte to GPIB convention
            self.strgpib = ' '
            if dATN:  # ATN, decode commands
                if dbyte == 0x01: self.strgpib = 'GTL'
                if dbyte == 0x04: self.strgpib = 'SDC'
                if dbyte == 0x05: self.strgpib = 'PPC'
                if dbyte == 0x08: self.strgpib = 'GET'
                if dbyte == 0x09: self.strgpib = 'TCT'
                if dbyte == 0x11: self.strgpib = 'LLO'
                if dbyte == 0x14: self.strgpib = 'DCL'
                if dbyte == 0x15: self.strgpib = 'PPU'
                if dbyte == 0x18: self.strgpib = 'SPE'
                if dbyte == 0x19: self.strgpib = 'SPD'
                if dbyte == 0x3f: self.strgpib = 'UNL'
                if dbyte == 0x5f: self.strgpib = 'UNT'
                if dbyte > 0x1f and dbyte < 0x3F:    # address Listener
                    self.strgpib = 'L' + chr(dbyte + 0x10)
                if dbyte > 0x3f and dbyte < 0x5F:    # address Talker
                    self.strgpib = 'T' + chr(dbyte - 0x10)
            else:
                if dbyte > 0x1f and dbyte < 0x7F: self.strgpib = chr(dbyte)
                if dbyte == 0x0a: self.strgpib = 'LF'
                if dbyte == 0x0d: self.strgpib = 'CR'
                    
            self.putb([1, [self.strgpib]])  # annotation row = 1
            self.strEOI = ' '
            if dEOI: 
                self.strEOI = 'EOI'
            self.putb([2, [self.strEOI]])  # annotation row = 2
            # to Python output
            #self.putpb(['ITEM', self.saved_item])
            #self.putpb(['GPIB', self.strgpib])
            if self.debug: print("{0:6d}; {1:02X};{2:>4d}; {3:4};{4:>4}".format(self.ss_item,dbyte,dbyte,self.strgpib,self.strEOI))

            self.ss_item = self.samplenum
            self.saved_item = item
            self.saved_ATN = item2
            self.saved_EOI = item3

        ws = 16 # must be 16 pins for GPIB

        # Get as many items as the configured wordsize says.
        if self.itemcount < ws:
            return

        self.itemcount, self.items = 0, []

    def find_clk_edge(self, clk, datapins):
        # Ignore sample if the clock pin hasn't changed.
        if clk == self.oldclk:
            return
        self.oldclk = clk
        # sample on falling clock edge
        if clk == 1: 
            return

        # Found the correct clock edge, now get the bits.
        self.handle_bits(datapins)

    def decode(self, ss, es, data):
        #if self.debug: print(self.samplenum, ' ', ss, ' ', es) # see the chunks
        lsn = self.options['sample_total']

        for (self.samplenum, pins) in data:
            if lsn > 0:
                if (lsn - self.samplenum) == 1:  # show last data word
                    self.handle_bits(pins[1:])

            # Ignore identical samples early on (for performance reasons).
            if self.oldpins == pins:
                continue
            self.oldpins = pins

            if sum(1 for p in pins if p in (0, 1)) == 0:
                raise ChannelError('At least one channel has to be supplied.')

            if pins[0] not in (0, 1):
                self.handle_bits(pins[1:])  
            else:
                self.find_clk_edge(pins[0], pins[1:])

