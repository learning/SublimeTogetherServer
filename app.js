var fs = require('fs'),
	net = require('net'),
	commands = require('./lib/commands'),
	handlers = require('./lib/handlers'),
	clients = [],
	buffers = {},
	archiver = require('archiver'),
	server;

/**
 * Handle socket data
 */
function handleData(socket, cmd, data) {
	var key;
	if (cmd in commands.in_cmd) {
		key = commands.in_cmd[cmd];
	} else {
		key = 'error';
		data = cmd;
	}
	handlers[key + 'Handler']({
		key    : cmd,
		data   : data,
		sender : socket,
		clients: clients
	});
}

function dataHandler(data) {
	var socket = this,
		// client's buffer stat
		buff = buffers[this.clientId];
	if (data) {
		buff.tmp = Buffer.concat([buff.tmp, data]);
	}
	switch (buff.step) {
		case 0: // read head
			if (buff.tmp.length >= 3) {
				if (buff.tmp[0] === 0xa9 && buff.tmp[1] === 0x5f &&
						buff.tmp[2] === 0xca) {
					buff.step = 1;
					buff.tmp = buff.tmp.slice(3);
					if (buff.tmp.length >= 1) {
						dataHandler.call(socket)
					}
				} else {
					// header not match, cut 1 byte and handle again
					buff.tmp = buff.tmp.slice(1);
					dataHandler.call(socket);
				}
			}
			break;
		case 1: // read command
			if (buff.tmp.length >= 1) {
				buff.cmd = buff.tmp[0];
				buff.tmp = buff.tmp.slice(1);
				buff.step = 2;
				if (buff.tmp.length >= 4) {
					dataHandler.call(socket);
				}
			}
			break;
		case 2: // read length
			if (buff.tmp.length >= 4) {
				buff.length = buff.tmp.readUInt32LE(0);
				buff.tmp = buff.tmp.slice(4);
				buff.step = 3;
				if (buff.tmp.length >= buff.length) {
					dataHandler.call(socket);
				}
			}
		break;
		case 3: // read data body
			if (buff.tmp.length >= buff.length) {
				handleData(socket, buff.cmd, buff.tmp.slice(0, buff.length));
				buff.tmp = buff.tmp.slice(buff.length);
				if (buff.tmp.length >= 3) {
					dataHandler.call(socket);
				}
			}
			buff.step = 0;
			delete buff.cmd;
			delete buff.length;
		break;
		default:
			buff.step = 0;
			dataHandler.call(socket);
			break;
	}
}

function errorHandler(err) {
	console.log(this.remoteAddress + ' disconnected.');
}

function disconnectHandler() {
	console.log(this.remoteAddress + ' disconnected.');
}

function serverHandler(socket) {
	console.log(socket.remoteAddress + ' connected.');
	socket.clientId = new Date().getTime();
	buffers[socket.clientId] = {
		tmp: new Buffer(0),
		step: 0
	};
	clients.push(socket);
	socket.on('end', disconnectHandler);
	socket.on('data', dataHandler);
	socket.on('error', errorHandler);
	handlers.sendMessage(socket, 'message', '[System]: Server connected');
}

function initProject() {
	var archive = archiver.create('zip');

	archive.on('error', function (err) {
		throw err;
	});

	// archive.pipe(output);

	archive.bulk({
		expand: true,
		src: ['project/**']
	});

	archive.finalize();
}

fs.readFile('config.json', function (err, data) {
	var config = JSON.parse(data);
	server = net.createServer(serverHandler).listen(config.port, function () {
		console.log('server running on port ' + config.port);
	});
});
