# sigrok-gpib
sigrok decoder gpib for 16 bit logic analyzer

For GPIB (General Purpose Interface Bus, or HPIB, or IEEE488; 16 bits parallel) analysis, used with a Saleae Logic16 clone.

The first picture shows in detail the GPIB handshake. 
![gpib handshake] (https://raw.githubusercontent.com/rudi48/sigrok-gpib/master/sigrok_decoder_gpib_handshake-940.png)

The second picture shows in detail the last 4 bytes, notice the EOI signal at the last data byte.
![gpib end of session] (https://raw.githubusercontent.com/rudi48/sigrok-gpib/master/sigrok_decoder_gpib_end-940.png)

The third picture shows the whole GPIB session: command ID, answer HP1631D. 
![gpib session] (https://raw.githubusercontent.com/rudi48/sigrok-gpib/master/sigrok_decoder_GPIB_940.png)

On the right you see a __picture__ of the '''gpib''' decoder __attributes__, seen when you click on the flag __gpib__ on the left in the __picture__ above.

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
![gpib decoder attribute mask] (https://raw.githubusercontent.com/rudi48/sigrok-gpib/master/sigrok_decoder_GPIB_attributes-349.png)


Installation
------------
```
mkdir -p ~/.local/share/libsigrokdecode/decoders
cd ~/.local/share/libsigrokdecode/decoders
git clone https://github.com/rudi48/sigrok-gpib.git gpib
```
