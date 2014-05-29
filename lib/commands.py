# commands from server
in_cmd = {
    0xd1: 'message',
    0xd2: 'open_file',
    0xd3: 'close_file',
    0xd4: 'change_selection',
    0xd5: 'edit_file'
}

# commands for send
out_cmd = {
    'initialize'      : 0xa0, # initialize project
    'message'         : 0xa1, # send messages
    'change_selection': 0xa4, # change selection
    'edit_file'       : 0xa5  # edit a file (buffer)
}