from reserve import find_app
from jsonrmc import handle

def Handler(root):
	def handle_request(socket, client_address, server):
		print ('New connection from %s:%s' % (client_address[0], client_address[1]))

		stream = socket.makefile('rw')
		for line in stream:
			stream.write(handle(root, line) + '\n')
			stream.flush()
	return handle_request
 
def launch(args):
	return Handler(find_app(args, 'jsonrmc handler.', 'root'))
