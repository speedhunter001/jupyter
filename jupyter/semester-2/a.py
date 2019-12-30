def writeMissingEntries(line):
    with open("logfile.log", 'w') as f:
        try:
            line_in_list = line.split(',')
            line_in_list[4]
        except IndexError:
            f.write(line)

