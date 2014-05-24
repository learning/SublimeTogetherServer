module.exports = {
	// commands from client
	in_cmd: {
		0xd1: 'message',
		0xd2: 'openFile',
		0xd3: 'closeFile',
		0xd4: 'changeSelection',
		0xd5: 'editFile'
	},

	// commands for send
	out_cmd: {
		'initialize'     : 0xa0, // initialize project
		'message'        : 0xa1, // send messages
		'changeSelection': 0xa4, // change selection
		'editFile'       : 0xa5  // edit a file (buffer)
	}
}