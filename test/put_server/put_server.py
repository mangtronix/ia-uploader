#!/opt/local/bin/python

"""Simple server to accept PUT requests for testing cross-origin PUTs

Michael Ang <http://github.com/mangtronix>
License: AGPL 3.0
"""

import string

import bottle
from bottle import *

def allowedOrigin():
	return '*'
	
def allowedMethods():
	return 'GET,PUT'

def allowedHeaders():

	# $$$ should mediatype be disallowed and automatically guessed?
	meta_headers = ['title', 'description', 'language', 'mediatype']
	meta_list_headers = ['collection']
	
	headers = [
		'authorization', 'x-amz-acl', 'x-amz-auto-make-bucket',
		'cache-control', 'x-requested-with',
		'x-file-name', 'x-file-size', 'x-archive-ignore-preexisting-bucket',		
	]
	
	meta_headers = ['x-archive-meta-%s' % header for header in meta_headers]
	headers.extend(meta_headers)
	
	max_list_members = 2
	list_headers = []
	for header in meta_list_headers:
		for i in range(max_list_members):
			list_headers.append('x-archive-meta%02d-%s' % (i + 1,header))
	headers.extend(list_headers)
	
	return string.join(headers, ',')

@route('/')
def index():
    return '<p><a href="/static/put.html">PUT</a> to /upload/filename</p><p>Allowed headers are %s<p>' % allowedHeaders()
    
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
