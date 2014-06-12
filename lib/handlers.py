import config
file_map = {}

def error_handler(key, data, pool, sender):
    print('Unknow Key Error: %s' % hex(key))
    print(data)

def login_handler(key, data, pool, sender):
    print('checking user...', data['user'] in config.users, data['pass'] == config.users[data['user']])
    if data['user'] in config.users and data['pass'] == config.users[data['user']]:
        for client in pool:
            if client.is_alive():
                if client is sender:
                    sender.send('message', '[System]: login successed.')
                    sender.user_name = data['user']
                else:
                    client.send('message', '%s connected.' % data['user'])
    else:
        sender.send('disconnect', '[System]: login failed.')
        sender.close()

def message_handler(key, data, pool, sender):
    for thread in pool:
        thread.send('message', '[%s]: %s' % (sender.user_name, data))

def send_client_list(path):
    client_list = list(map(lambda c: c.user_name, file_map[path]))
    for client in file_map[path]:
        client.send('update_client_list', {
            'path': path,
            'client_list': client_list
            })

def open_file_handler(key, data, pool, sender):
    if data in file_map:
        # file not open yet
        file_map[data].append(sender)
    else:
        # file opened
        file_map[data] = [sender]
    send_client_list(data)
    # print('file_map:\n', file_map)

def close_file_handler(key, data, pool, sender):
    if data in file_map:
        file_map[data].remove(sender)
        if len(file_map[data]) is 0:
            del(file_map[data])
        else:
            send_client_list(data)
    
    # print('file_map:\n', file_map)

def change_selection_handler(key, data, pool, sender):
    path = data['path'] # file's path
    sels = data['selections'] # selections
    if path in file_map:
        for client in file_map[path]:
            if client is not sender and client.is_alive():
                client.send('change_selection', {
                    'client': sender.user_name,
                    'path': path,
                    'selections': sels
                    })
    # print('%s change selection: %s' % (sender.address[0], path))

def edit_file_handler(key, data, pool, sender):
    path = data['path']
    patch = data['patch']
    region_dict = data['region_dict']
    if path in file_map:
        for client in file_map[path]:
            if client is not sender and client.is_alive():
                client.send('edit_file', {
                    'client': sender.user_name,
                    'path': path,
                    'patch': patch,
                    'region_dict': region_dict
                    })
    # print('%s edit_file: %s\npatch:\n%s' % (sender.address[0], path, patch))
