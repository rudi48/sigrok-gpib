# sigrok-gpib
sigrok decoder gpib for 16 bit logic analyzer

For GPIB (General Purpose Interface Bus, or HPIB, or IEEE488; 16 bits parallel) protocol analysis, used with a Saleae Logic16 clone.

The first picture shows in detail the GPIB handshake. 

![gpib handshake](https://github.com/rudi48/sigrok-gpib/blob/master/sigrok_decoder_gpib_handshake-940.png)

The second picture shows in detail the last 4 bytes, notice the EOI signal at the last data byte.

![gpib end of session](https://raw.githubusercontent.com/rudi48/sigrok-gpib/master/sigrok_decoder_gpib_end-940.png)

The third picture shows the whole GPIB session: command ID, answer HP1631D. 

![gpib session](https://raw.githubusercontent.com/rudi48/sigrok-gpib/master/sigrok_decoder_GPIB_940.png)

<img align="right" src="https://raw.githubusercontent.com/rudi48/sigrok-gpib/master/sigrok_decoder_GPIB_attributes-349.png">

On the right you see a __picture__ of the __gpib__ decoder __attributes__, seen when you click on the flag __gpib__ on the left in the __picture__ above.

The following is important:
 * total number of samples: must be set, in order to decode the last byte.
 * channel __ATN__: must be set to pin __14__
 * channel __CLK__: must be set to pin __DAV__

The __total number of bytes__ 20000 was from the __capture session__:
 * 20 k samples at 500 KHz sample rate = 40 ms

A short explanation for the GPIB command decoding, when line __ATN__ was active:
 * L4 = set device with GPIB address 4 to __Listener__
 * T4 = set device with GPIB address 4 to __Talker__
 * UNL = UNLISTEN
 * UNT = UNTALK
 * LF = LineFeed (end of line)
 * EOI = End Or Identify
  

### GPIB State Analysis
If you set in __attributes window__ the __state analysis flag__ to True, you will get in the terminal the following print, like a 
__State Analysis__:
```
GPIB State Analysis
     0; 3F;  63; UNL ;
     9; 5F;  95; UNT ;
    18; 24;  36; L4  ;
    25; 49;  73; I   ;
  4031; 44;  68; D   ;
  5843; 0A;  10; LF  ; EOI
  5852; 3F;  63; UNL ;
  5860; 5F;  95; UNT ;
  5869; 44;  68; T4  ;
 14830; 48;  72; H   ;
 15417; 50;  80; P   ;
 15536; 31;  49; 1   ;
 15656; 36;  54; 6   ;
 15775; 33;  51; 3   ;
 15895; 31;  49; 1   ;
 16106; 44;  68; D   ; EOI
 16123; 3F;  63; UNL ;
 16130; 5F;  95; UNT ;
```
The __data colums__ are: 
 * sample number, in our case * 2µs = [µs], total session length = 40,000 µs
 * data byte in hexadecimal
 * data byte in decimal
 * ASCII or gpib decoding
 * EOI flag

The __logic__ of the GPIB session is:
 * Controller set the GPIB to UNLISTEN and UNTALK (neutral state)
 * Controller set Device with GPIB address number 4 to LISTEN
 * Controller send command 'ID LF+EOI' to Device with GPIB address number 4 (request Idendity string)
 * Controller set the GPIB to UNLISTEN and UNTALK (neutral state)
 * Controller set Device with GPIB address number 4 to TALK
 * Device with GPIB address number 4 send the ID string 'HP1631D+EOI' to Controller
 * Controller set the GPIB to UNLISTEN and UNTALK (neutral state)
  

### Installation for Linux
```
mkdir -p ~/.local/share/libsigrokdecode/decoders
cd ~/.local/share/libsigrokdecode/decoders
git clone https://github.com/rudi48/sigrok-gpib.git gpib

# the samples pictures are made with the session file:
$ pulseview -i hp1631ID.sr

# a quick test for a good installation, and showing the parameters is:
$  sigrok-cli --protocol-decoders gpib --show
ID: gpib
Name: GPIB
Long name: General Purpose Interface Bus
Description: IEEE-488 GPIB / HPIB protocol.
License: gplv2+
Annotation classes:
- items: Items
- gpib: DAT/CMD
- eoi: EOI
Annotation rows:
- bytes (Bytes): items
- gpib (DAT/CMD): gpib
- eoi (EOI): eoi
Required channels:
- d0 (D0): Data I/O bit 1, ch 0
- d1 (D1): Data I/O bit 2, ch 1
- d2 (D2): Data I/O bit 3, ch 2
- d3 (D3): Data I/O bit 4, ch 3
- d4 (D4): Data I/O bit 5, ch 4
- d5 (D5): Data I/O bit 6, ch 5
- d6 (D6): Data I/O bit 7, ch 6
- d7 (D7): Data I/O bit 8, ch 7
- eoi (EOI8): End or identify, ch 8
- dav (DAV9): Data valid (clock), ch 9
- nrfd (NRFD10): Not ready for data, ch 10
- ndac (NDAC11): Not data accepted, ch 11
- ifc (IFC12): Interface clear, ch 12
- srq (SRQ13): Service request, ch 13
- atn (ATN14): Attention, ch 14
- ren (REN15): Remote enable, ch 15
Optional channels:
None.
Options:
- sample_total: Total number of samples (default 0)
- state: state analysis ('False', 'True', default 'False')
Documentation:
This protocol decoder can decode the GPIB (IEEE-488) protocol.

If the clock channel DAV is set, GPIB decoding is shown.

If the total sample number is given, the last byte is shown.

If option "state" is set "True", a GPIB "State Analysis" is printed
in the terminal.
```

[More information about you will find in the "Github Wiki" or on my homepage](http://www.rudiswiki.de/wiki9/SigrokDecoderGPIB)
