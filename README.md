# sigrok-gpib
sigrok decoder gpib for 16 bit logic analyzer

For GPIB (General Purpose Interface Bus, or HPIB, or IEEE488; 16 bits parallel) analysis, used with a Saleae Logic16 clone.

The first picture shows in detail the GPIB handshake. 
![gpib handshake] (https://raw.githubusercontent.com/rudi48/sigrok-gpib/master/sigrok_decoder_gpib_handshake-940.png)

The second picture shows in detail the last 4 bytes, notice the EOI signal at the last data byte.
![gpib end of session] (https://raw.githubusercontent.com/rudi48/sigrok-gpib/master/sigrok_decoder_gpib_end-940.png)

The third picture shows the whole GPIB session: command ID, answer HP1631D. 
![gpib session] (https://raw.githubusercontent.com/rudi48/sigrok-gpib/master/sigrok_decoder_GPIB_940.png)

This is the sigrok decoder attribute mask.
![gpib decoder attribute mask] (https://raw.githubusercontent.com/rudi48/sigrok-gpib/master/sigrok_decoder_GPIB_attributes-349.png)


Installation
------------
```
mkdir -p ~/.local/share/libsigrokdecode/decoders
cd ~/.local/share/libsigrokdecode/decoders
git clone https://github.com/vooon/sigrok-rgb_led_ws281x.git rgb_led_ws281x
```
