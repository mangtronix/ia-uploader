#!/opt/local/bin/python

"""Simple server to accept PUT requests for testing cross-origin PUTs

Michael Ang <http://github.com/mangtronix>
License: AGPL 3.0
"""

import bottle
from bottle import *

def allowedOrigin():
	return '*'
	
def allowedMethods():
	return 'GET,PUT'

def allowedHeaders():
	return 'authorization,cache-control,x-amz-acl,x-amz-auto-make-bucket,x-file-name,x-file-size,x-requested-with'

@route('/')
def index():
    return '<p>PUT to /upload/filename</p>'
    
@route('/static/<filepath:path>')
def server_static(filepath):
	return static_file(filepath, root='./static') # relative to directory server called from

@route('/upload/:filename', method='OPTIONS')
def upload_options(filename=None):
	print("OPTIONS request for %s" % filename)
		
	response.set_header('Access-Control-Allow-Origin', allowedOrigin())
	response.set_header('Access-Control-Allow-Methods', allowedMethods())
	response.set_header('Access-Control-Allow-Headers', allowedHeaders())
	response.set_header('Access-Control-Max-Age', 60*24*7) # One week - only applies if putting same file so not very useful
	
	return ""
	
@route('/upload/:filename', method='PUT')
def upload_put(filename=None):
	print("PUT request for %s" % filename)
	
	response.set_header('Access-Control-Allow-Origin', allowedOrigin())
	response.set_header('Access-Control-Allow-Methods', allowedMethods())
	response.set_header('Access-Control-Allow-Headers', allowedHeaders())

	out_filename = os.path.join('upload', filename)
	content_length = int(request.get_header('Content-Length'))
	
	print("  Reading %d bytes to %s" % (content_length, out_filename))
	out_file = open(out_filename, 'wb')
	out_file.write(request['wsgi.input'].read(content_length))
	out_file.close()
	request['wsgi.input'].close()

	return "Created %s with %d bytes\n" % (out_filename, content_length)
	
@route('/upload/:filename', method='GET')
def upload_get(filename=None):
	print("GET request for %s" % filename)
	return "File %s" % filename
	
if __name__ == "__main__":
	bottle.debug(True)
	run(host='', port=8080, reloader=True)
