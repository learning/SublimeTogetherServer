var commands = require('./commands'),
	fileMap = {};

/**
 * Send data to the client
 * @param socket client's socket
 * @param cmd  command
 * @param data data body
 */
function send(socket, cmd, data) {
	if (data instanceof Buffer) {
		var head = new Buffer(8);
		head[0] = 0xd0;
		head[1] = 0x02;
		head[2] = 0x0f;
		head[3] = commands.out_cmd[cmd];
		head.writeUInt32LE(data.length, 4);
		socket.write(head);
		socket.write(data);
	} else {
		if (typeof data === 'string') {
			send(socket, cmd, new Buffer(data));
		} else {
			console.error('data is not a buffer', data);
		}
	}
}

module.exports = {
	errorHandler: function (arg) {
		var key = arg.key.toString(16);
		if (key.length === 1) {
			key = '0' + key;
		}
		key = '0x' + key;
		console.error('[Error] Unknow key ' + key);
	},

	messageHandler: function (arg) {
		arg.clients.forEach(function (client) {
			send(client, 'message', '[' + arg.sender.remoteAddress + '] ' +
				arg.data.toString());
		});
	},

	openFileHandler: function (arg) {
		var path = arg.data.toString();
		if (!fileMap[path]) {
			// create map and add current sender to the map
			fileMap[path] = [arg.sender];
		} else {
			// just add current sender to the map
			fileMap[path].push(arg.sender);
		}
		console.log(arg.sender.remoteAddress + ' open a file: ' + arg.data.toString());
	},

	closeFileHandler: function (arg) {
		var path = arg.data.toString();
		if (fileMap[path]) {
			for (var i = fileMap[path].length - 1; i >= 0; i--) {
				if (fileMap[path][i] === arg.sender) {
					fileMap[path].splice(i, 1);
				}
			}
		}
		console.log(arg.sender.remoteAddress + ' close a file: ' + arg.data.toString());
	},

	changeSelectionHandler: function (arg) {
		try {
			var o = JSON.parse(arg.data.toString()),
				path = o.path, // file's path
				sels = o.selections; // selections
			if (fileMap[path]) {
				fileMap[path].forEach(function (client) {
					if (client !== arg.sender) {
						// send to other clients
						send(client, 'changeSelection', JSON.stringify({
							client: arg.sender.remoteAddress,
							path: path,
							selections: sels
						}));
					}
				});
			}
			console.log(arg.sender.remoteAddress + ' change selection: ' + o.path);
			console.log(o.selections);
		} catch (err) {
			console.error('changeSelectionHandler', err);
			console.log(arg.data.toString());
		}
	},

	editFileHandler: function (arg) {
		try {
			var o = JSON.parse(arg.data.toString()),
				path = o.path,
				patch = o.patch;
			if (fileMap[path]) {
				fileMap[path].forEach(function (client) {
					if (client !== arg.sender) {
						send(client, 'editFile', JSON.stringify({
							client: arg.sender.remoteAddress,
							path: path,
							patch: patch
						}));
					}
				});
			}
		} catch (err) {
			console.error('editFileHandler', err);
			console.error(arg.data.toString());
		}
	},

	sendMessage: send
};

