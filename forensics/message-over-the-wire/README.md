This challenge consists of a packet capture between a wired keyboard and a laptop.

The flag is the keys that were pressed by the keyboard and sent to the laptop.

To isolate these in wireshark, you can use:
``` wireshark
usb.transfer_type == 0x01 && usb.endpoint_address.direction == "IN" && usb.bInterfaceClass==0x03 && usb.src == 3.12.1
```

This  only shows:
 - transfer type `URB_INTERRUPT`s (sudden signals from the keyboard such as user input)
 - direction `IN` aka only into the computer and not back to the keyboard
 - interface class of `HID` (human interface devices, e.g. keyboards, mice, and trackpads)
 - only from the usb device `3.12` (the keyboards address)

Looking at the packets then, every roughly second packet contains a character sent through in it (in the `HID Data` field) (in their hex keyboard codes).

All these packets can then be exported into a csv `data.csv`

Below a python program has been written for when you extract all of the keycodes into a file, to convert them to their actual characters (and get the flag).


Solving script:

``` python
# yes I typed this by hand
mapping = {
    0x04: ("a", "A"), 0x05: ("b", "B"), 0x06: ("c", "C"), 0x07: ("d", "D"),
    0x08: ("e", "E"), 0x09: ("f", "F"), 0x0A: ("g", "G"), 0x0B: ("h", "H"),
    0x0C: ("i", "I"), 0x0D: ("j", "J"), 0x0E: ("k", "K"), 0x0F: ("l", "L"),
    0x10: ("m", "M"), 0x11: ("n", "N"), 0x12: ("o", "O"), 0x13: ("p", "P"),
    0x14: ("q" ,"Q"), 0x15: ("r", "R"), 0x16: ("s", "S"), 0x17: ("t" ,"T"),
    0x18: ("u", "U"), 0x19: ("v", "V"), 0x1A: ("w", "W"), 0x1B: ("x", "X"),
    0x1C: ("y", "Y"), 0x1D: ("z", "Z"),
    0x1E: ("1" ,"!"), 0x1F: ("2", "@"), 0x20: ("3", "#"), 0x21: ("4", "$"),
    0x22: ("5", "%"), 0x23: ("6", "^"), 0x24: ("7", "&"), 0x25: ("8", "*"),
    0x26: ("9", "("), 0x27: ("0", ")"),
    0x28: ("ENTER", "ENTER"), 0x2A: ("DELETE", "DELETE"), 0x2B: ("TAB", "TAB"), 0x2C: ("SPACEBAR" ,"SPACEBAR"),
    0x2D: ("-", "_"), 0x2E: ("=", "+"), 0x2F: ("[", "{"), 0x30: ("]", "}"),
    0x31: ("\\", "|"), 0x33: (";", ":"), 0x34: ("'", "'"), 0x36: (",", "<"),
    0x37: (".", ">"), 0x38: ("/" ,"?") 
}

FILE = "data.csv"
with open(FILE, "r") as file:
    for line in file:
        line = line.split(",")[7]
        if not line or len(line.strip()) != 16:
            continue
        
        result = ""
        modifier = int(line[:2], 16)
        keycode = int(line[4:6], 16)

        if keycode == 0x00:
            continue
        
        if modifier in (0x02, 0x20):
            print(mapping[keycode][1], end="")
        elif modifier in (0x01, 0x10):
            print("CTRL")
        else:
            print(mapping[keycode][0], end="")
```

Source:
<https://motasem-notes.net/usb-keystrokes-analysis-with-wireshark-hackthebox-logger-ctf-walkthrough/>
<https://hacktricks.wiki/en/generic-methodologies-and-resources/basic-forensic-methodology/pcap-inspection/usb-keystrokes.html>
<https://wiki.osdev.org/USB_Human_Interface_Devices?utm_source=chatgpt.com>
<https://github.com/adafruit/Adafruit_TinyUSB_Arduino/tree/master/examples/HID>
<https://www.anquanke.com/post/id/85218>
<https://forum.arduino.cc/t/hid-keyboard-key-codes/1011438>
<https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf>
<https://github.com/tmk/tmk_keyboard/wiki/USB:-HID-Usage-Table>
<https://gist.github.com/ekaitz-zarraga/2b25b94b711684ba4e969e5a5723969b>
<https://github.com/zlittell/USBHIDKeycodes/tree/main>
<https://docs.arduino.cc/language-reference/en/functions/usb/Keyboard/keyboardModifiers/>