def tail( f, lines=20 ):
    '''
     csv_tools aims to make reading csv file more convinentpublic_pizo_preip
    '''
    total_lines_wanted = lines

    BLOCK_SIZE = 5024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
                # from the end of the file
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            # read the last block we haven't yet read
            f.seek(block_number*BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count('\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = ''.join(reversed(blocks))
    return '\n'.join(all_read_text.splitlines()[-total_lines_wanted:])
#def tail_linux(f,lines=1):
    
def get_one_line(f):
    '''
    get_one_line is used to get the first line from a file
    '''
    with open(f, 'r') as myfile:
        public_pizo_pre=myfile.read().replace('\n', '')
    return public_pizo_pre


def get_first_line(f):
    '''
    get_one_line is used to get the first line from a file
    '''
    with open(f, 'r') as f:
        first_line = f.readline()
    return first_line
