import sys

BANKS = [
    "abcdefghijklmn",
    "opqrstuvwxyz.,",
    '!?-/()&"\'\n'
]
ALLCHARS = ''.join(BANKS)
CODES = [
    "onecap",
    "lower",
    "upper",
    "digit"
]

def tinyify(text):
    def getnextlastcap(text, index):
        for i in range(index, len(text)):
            if text[i].islower():
                return i
        return -1
    def getvaluesforchar(char, currentbank):
        if char.isdigit():
            return [format(int(char), "04b")], currentbank  # if the character is a digit, return the 4 bit binary representation of the digit and the current bank
        char = char.lower()                             # make the character lowercase (we've already checked for caps at this point)
        foundbank = None
        for i, bank in enumerate(BANKS):
            if char in bank:
                foundbank = i                           # locate the bank that contains the desired character
                break                                   # stop looking once we've found it
        if foundbank is None:                           # this should not happen but if it does it's not a big deal,
            return []                                   # we can just return an empty list
        steps = (foundbank - currentbank) % len(BANKS)  # calculate the number of bank switches needed to reach desired bank
        output = ["1111"] * steps                       # add a corresponding amount of switch codes to the output values
        charindex = BANKS[foundbank].index(char)        # get the index number of the char within the bank
        charindex = format(charindex, "04b")            # convert index number to 4 bit binary string
        output.append(charindex)                        # finally add char value to the output (if no switches are needed, this will be the only value)
        return output, foundbank
    
    def converttobin(tiniedtext, beforelength):
        filelength = len(tiniedtext)
        if filelength % 2 != 0:                                                 # if there is an odd number of nibbles we should make it even so we can convert to bytes
            tiniedtext.append("0000")                                           # add a 0 nibble to the end of the file
        header = format(filelength, "032b")                                     # create a 32 bit binary header with the length of the file
        print(header)
        header = [header[i:i+4] for i in range(0, len(header), 4)]         # split the 32 bit header into 8 nibbles (dynamic)
        tiniedtext = header + tiniedtext                                        # add the header to the beginning of the file data
        print(tiniedtext)
        filebytes = []
        for i in range(0, len(tiniedtext)-1, 2):                                # iterate through the file in pairs
            byte = tiniedtext[i] + tiniedtext[i + 1]                            # combine two nibbles into a byte
            byte = int(byte, 2)                                                 # convert the byte to an integer
            if byte > 255:                                                      # if the byte is greater than 255, something went wrong
                print("ERROR: byte too big for he got damn feet") 
            filebytes.append(byte)                                              # add the byte to the list of bytes
        print(f"File reduced by {(beforelength * 8) - (len(filebytes) * 8)} bits")
        return filebytes
        # filename = "test"#input("Enter the name you want to use for the output file: ")
        # try:
        #     with open(f"{filename}.tiny", "wb") as f:
        #         f.write(bytes(filebytes))                                       # write the bytes to a file
        #     print(f"File saved as {filename}.tiny")
        #     print(f"File reduced by {(beforelength * 8) - (len(filebytes) * 8)} bits")
        # except Exception as e:
        #     print(f"An error occurred: {e}")
        #     return
        
        
    
    beforelength = len(text)

    tiniedtext = []
    currentbank = 0
    charmode = "lower"

    for i, char in enumerate(text):
        print(char)
        charvalues = []
        if char.lower() not in ALLCHARS:
            continue
        if char.isupper() and not charmode == "upper":
            nextlastcap = getnextlastcap(text, i)
            if nextlastcap != -1:
                if (nextlastcap - i) > 1:                               # if there is more than one capital letter in a row, switch to upper mode
                    charmode = "upper"
                    modeindex = format(CODES.index(charmode), "04b")
                    charvalues.extend(["1110", modeindex])
                else:                                                   # if there is only one capital letter, switch to onecap mode
                    charmode = "onecap"
                    modeindex = format(CODES.index(charmode), "04b")
                    charvalues.extend(["1110", modeindex])
                    charmode = "lower"                                  # switch back to lowercase after onecap mode
        elif char.islower() and not charmode == "lower":
            charmode = "lower"                                          # switching to lowercase if needed
            modeindex = format(CODES.index(charmode), "04b")
            charvalues.extend(["1110", modeindex])
        elif char.isdigit() and not charmode == "digit":
            charmode = "digit"                                          # switching to digit mode if needed
            modeindex = format(CODES.index(charmode), "04b")
            charvalues.extend(["1110", modeindex])
            charmode = "lower"                                          # switching back to lowercase after digit mode
        newvalues, currentbank = getvaluesforchar(char, currentbank)                                  
        charvalues.extend(newvalues)
        print(charvalues)
        print(f"charmode: {charmode}")
        tiniedtext.extend(charvalues)
    return converttobin(tiniedtext, beforelength)
        
if __name__ == "__main__":
    import bigifier
    sampletext = """Lore hidden in plain sight often carries the most weight.
    Patterns emerge, connections are made,
    yet the meaning eludes comprehension.

    Words drift through time,
    shaping the unseen framework of our understanding.
    """
    tinyify(sampletext)