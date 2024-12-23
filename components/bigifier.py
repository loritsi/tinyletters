CODES = [
    "onecap",
    "lower",
    "upper",
    "digit"
]

def bigify(tinybytes, BANKS, CODES=CODES):
    nibbles = []
    header = tinybytes[:4]                                      # get the header (the first 4 bytes)
    for i, byte in enumerate(header):
        byte = format(byte, "08b")                              # turn each byte of the header into a binary string
        header[i] = byte                                        # replace the byte with the binary string
    header = ''.join(header)                                    # squish the header segments into a single string
    filelength = int(header, 2)                                 # convert the header to an integer
    for byte in tinybytes[4:]:                                  # go through each byte, skipping the header
        byte = format(byte, "08b")                              # turn each byte into a binary string
        byte = [byte[i:i+4] for i in range(0, len(byte), 4)]    # split the byte into 2 nibbles
        nibbles += byte                                         # add the nibbles to the list   
    if filelength % 2 != 0:                                     # if the file length is odd
        nibbles.pop()                                           # remove the last nibble (it's a padding nibble)

    currentbank = 0                                             # start in the first bank (0)
    charmode = "lower"                                          # start in lowercase mode
    chars = []                                                  # create an empty list to store the characters
    for i, nibble in enumerate(nibbles):
        if charmode == "waiting":                           # if we're waiting for a control code
            nibble = int(nibble, 2)
            charmode = CODES[nibble]
            continue                                        # we're done with this nibble

        elif nibble == "1111":                              # if the nibble is a switch code
            currentbank = (currentbank + 1) % len(BANKS)    # switch to the next bank, wrapping around if needed
            continue                                        # we're done with this nibble

        elif nibble == "1110":
            charmode = "waiting"                            # set the charmode to waiting for a control code
            continue                                        # we're done with this nibble

        elif charmode == "digit":                           # if we're in digit mode
            char = int(nibble, 2)                           # convert the nibble to an integer directly
        
        else:                                               # if we're not a control code, switch code, or digit
            char = BANKS[currentbank][int(nibble, 2)]       # get the character from the current bank
            if charmode == "upper":                         # if we're in uppercase mode
                char = char.upper()                         # make the character uppercase
            elif charmode == "onecap":                      # if we're in onecap mode
                char = char.upper()                         # make the character uppercase
                charmode = "lower"                          # switch to lowercase mode
            chars.append(char)                              # we shouldn't need to do anything for lowercase mode 
                                                            # because the characters are already lowercase in the banks
    result = ''.join(chars)                                 # squish the characters into a string
    return result