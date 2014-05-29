file_map = {}

def error_handler(key, data, pool, sender):
    print('Unknow Key Error: %s' % hex(key))
    print(data)

def message_handler(key, data, pool, sender):
    for thread in pool:
        thread.send('message', '[%s]: %s' % (sender.address[0], data))

def open_file_handler(key, data, pool, sender):
    if data in file_map:
        # file not open yet
        file_map[data].append(sender)
    else:
        # file opened
        file_map[data] = [sender]
    # print('file_map:\n', file_map)

def close_file_handler(key, data, pool, sender):
    if data in file_map:
        del(file_map[data])
    # print('file_map:\n', file_map)

def change_selection_handler(key, data, pool, sender):
    path = data['path'] # file's path
    sels = data['selections'] # selections
    if path in file_map:
        for client in file_map[path]:
            if client is not sender and client.is_alive():
                client.send('change_selection', {
                    'client': sender.address[0],
                    'path': path,
                    'selections': sels
                    })
    # print('%s change selection: %s' % (sender.address[0], path))

def edit_file_handler(key, data, pool, sender):
    path = data['path']
    patch = data['patch']
    if path in file_map:
        for client in file_map[path]:
            if client is not sender and client.is_alive():
                client.send('edit_file', {
                    'client': sender.address[0],
                    'path': path,
                    'patch': patch
                    })
    # print('%s edit_file: %s\npatch:\n%s' % (sender.address[0], path, patch))
