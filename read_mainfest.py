def read_manifest(file_location):
    manifest = []
    
    # opening and reading the manifest, storing the lines
    file = open(file_location, 'r')
    lines = file.readlines()
    file.close()

    # organizing the data
    for line in lines:
        cell = read_line(line.strip()) # strip to get rid of spacing
        location, weight, title = cell
        weight = float(weight) # convert from a string to numerical value

    manifest.append([location, weight, title])
    return manifest

def read_line(line):
    strings = []
    curr = ""

    for char in line: # go char by char to get the different parts of the line
        if char == ",":
            strings.append(curr)
            curr = ""
        else:
            curr += char

    strings.append(curr) # need to append the last string
    return(strings)