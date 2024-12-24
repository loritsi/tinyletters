
CODES = [
    "onecap",
    "lower",
    "upper",
    "digit"
]

def tinyify(text, BANKS, ALLCHARS, CODES=CODES, debug=False):
    def getnextlastcap(text, index):
        for i in range(index, len(text)):
            if text[i].islower():
                return i
        return -1
    def getvaluesforchar(char, currentbank):
        if char.isdigit():
            return [format(int(char), "04b")], currentbank  # if the character is a digit, return the 4 bit binary representation of the digit and the current bank
        char = char.lower()                                 # make the character lowercase to match the banks (we've already checked for caps at this point)
        foundbank = None
        for i, bank in enumerate(BANKS):
            if char in bank:
                foundbank = i                           # locate the bank that contains the desired character
                break                                   # stop looking once we've found it
        if foundbank is None:                           # this should not happen but if it does it's not a big deal,
            return [], currentbank                      # we can just return an empty list and the current bank (we aren't going to move)
        steps = (foundbank - currentbank) % len(BANKS)  # calculate the number of bank switches needed to reach desired bank
        output = ["1111"] * steps                       # add a corresponding amount of switch codes to the output values
        charindex = BANKS[foundbank].index(char)        # get the index number of the char within the bank
        charindex = format(charindex, "04b")            # convert index number to 4 bit binary string
        output.append(charindex)                        # finally add char value to the output (if no switches are needed, this will be the only value)
        return output, foundbank                        # return the output values and the bank the character was found in (so we can keep track of it)
    
    def converttobin(tiniedtext, beforelength, debug=False):
        filelength = len(tiniedtext)                                            # get the length of the converted nibble list
        if filelength % 2 != 0:                                                 # if there is an odd number of nibbles we should make it even so we can convert to bytes
            tiniedtext.append("0000")                                           # add a 0 nibble to the end of the file
        header = format(filelength, "032b")                                     # create a 32 bit binary header with the length of the file
        header = [header[i:i+4] for i in range(0, len(header), 4)]              # split the header into nibbles (dynamic)
        tiniedtext = header + tiniedtext                                        # add the header to the beginning of the file data
        filebytes = []                                                              # create an empty list to store the bytes   
        for i in range(0, len(tiniedtext)-1, 2):                                    # iterate through the file in pairs
            byte = tiniedtext[i] + tiniedtext[i + 1]                                # combine two nibbles into a byte
            byte = int(byte, 2)                                                     # convert the byte to an integer
            if byte > 255:                                                                  # if the byte is above 255, something went wrong
                print(f"ERROR: byte exceeds 255 somehow, value: {byte}, capping at 255 ({byte % 256})")    # print an error message and move on
                byte = byte % 256                                                           # cap the byte at 255, hopefully by doing modulo it can recover whatever messed up garbage byte it was
            filebytes.append(byte)  # add the byte to the list of bytes
        if debug:                                                                       
            print(f"File reduced by {(beforelength * 8) - (len(filebytes) * 8)} bits")  # brag about how much we reduced the file
        return filebytes
    
    beforelength = len(text)
    tiniedtext = []
    currentbank = 0             # start in the first bank
    charmode = "lower"          # start in lowercase mode

    for i, char in enumerate(text):
        charvalues = []
        if char.lower() not in ALLCHARS:
            continue
        if char.isupper() and charmode != "upper":
            nextlastcap = getnextlastcap(text, i)
            if nextlastcap != -1:
                if (nextlastcap - i) > 1:                               # if there is more than one capital letter in a row, switch to upper mode
                    charmode = "upper"
                    modeindex = format(CODES.index(charmode), "04b")    # get the index of the mode
                    charvalues.extend(["1110", modeindex])              # add the control code and mode index to the output
                else:                                                   # if there is only one capital letter, switch to onecap mode
                    charmode = "onecap"
                    modeindex = format(CODES.index(charmode), "04b")
                    charvalues.extend(["1110", modeindex])
                    charmode = "lower"                                  # switch back to lowercase after onecap mode
        elif char.islower() and charmode != "lower":
            charmode = "lower"                                          # switching to lowercase if needed
            modeindex = format(CODES.index(charmode), "04b")
            charvalues.extend(["1110", modeindex])
        elif char.isdigit() and charmode != "digit":
            charmode = "digit"                                          # switching to digit mode if needed
            modeindex = format(CODES.index(charmode), "04b")
            charvalues.extend(["1110", modeindex])
            charmode = "lower"                                          # switching back to lowercase after digit mode
        newvalues, currentbank = getvaluesforchar(char, currentbank)                                  
        charvalues.extend(newvalues)
        tiniedtext.extend(charvalues)
    bintext = converttobin(tiniedtext, beforelength, debug=debug)
    afterlength = len(bintext)
    return bintext, beforelength, afterlength

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
