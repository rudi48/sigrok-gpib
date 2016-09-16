# sigrok-gpib
sigrok decoder gpib for 16 bit logic analyzer

For GPIB (General Purpose Interface Bus, or HPIB, or IEEE488; 16 bits parallel) analysis, used with a Saleae Logic16 clone.

The first picture shows in detail the GPIB handshake. 
![gpib handshake] (https://raw.githubusercontent.com/rudi48/sigrok-gpib/sigrok_decoder_gpib_handshake-940.png)

![PulseView start](https://raw.githubusercontent.com/vooon/sigrok-rgb_led_ws281x/master/pulseview-start.png)

![PulseView end](https://raw.githubusercontent.com/vooon/sigrok-rgb_led_ws281x/master/pulseview-end.png)


Installation
------------
```
mkdir -p ~/.local/share/libsigrokdecode/decoders
cd ~/.local/share/libsigrokdecode/decoders
git clone https://github.com/vooon/sigrok-rgb_led_ws281x.git rgb_led_ws281x
```
