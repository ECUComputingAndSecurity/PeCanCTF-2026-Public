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
        # get the HID from the csv, and remove the quotation marks
        line = line.split(",")[7][1:-1]
        # don't do the title
        if not line or len(line.strip()) != 16:
            continue

        # split into keycode, and the modifier that might also be down e.g. shift
        result = ""
        modifier = int(line[:2], 16)
        keycode = int(line[4:6], 16)

        # ignore empty packets
        if keycode == 0x00:
            continue
        
        if modifier in (0x02, 0x20):
            print(mapping[keycode][1], end="")
        elif modifier in (0x01, 0x10):
            print("CTRL")
        else:
            print(mapping[keycode][0], end="")