# -*- GeniTravel-Abou -*-
# -*- Lab-690 -*- 
import sqlite3
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn

from os import curdir, sep
import Cookie
import datetime
import time
import hashlib
import cgi

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	#Handler for the GET requests
	def do_GET(self):

		msg = 'not logged in'
		logged = False
		if "cookie" in self.headers:

			c = Cookie.SimpleCookie(self.headers["cookie"])

			_login = c['profile'].value
			_hash = c['hash'].value
			
			con = sqlite3.connect('users.db')
			cur = con.cursor()
			cur.execute('SELECT * FROM users')
			for row in cur.fetchall():
				(id, login, password, fname, lname, hash) = row
				if _login == login and _hash == hash:
					msg = 'logged as: ' + login
					logged = True
					break
			con.close()

		if self.path=="/" :
			self.path="/index.html"
		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html") and logged == False:
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				self.wfile.write("You are %s !" % msg)
				f.close()
			else:
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">')
				self.wfile.write('<link rel="stylesheet" type="text/css" href="style.css">')
				self.wfile.write('<h4 class = "form-signin-heading"> Logged as: ' + _login + "</h4>")
				self.wfile.write('<center>\
				<div class="wrapper">\
				<div class="push">\
				<h2>Profile page</h2>\
				<div class = "container">\
				<form class = "form-signin" role = "form" \
				action = "/logout" \
				method = "post">\
				<button class = "btn btn-lg btn-primary btn-block" type = "submit" \
					name = "action" value="logout">Logout</button>\
				</form>\
				</div> <!-- Container -->\
				</div> <!-- push -->\
				</div> <!-- Wrapper -->	 \
				</center>\
				')
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
		

	#Handler for the POST requests
	def do_POST(self):
		print("POST request")
		if self.path == "/logout":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})
			cookieExpiration = 1 * 20 # 20 sec
			expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=cookieExpiration)

			self.send_response(301)

			self.send_header('Refresh','5; url="/"')#refresh:" . $timeout . "; url=login.php
			
			
			cookie = Cookie.SimpleCookie(self.headers["cookie"])
			cookie['profile']['expires'] = -1
			cookie['hash']['expires'] = -1
			self.wfile.write(cookie.output())
			self.end_headers()
		elif self.path == "/register":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})
			(username, password, firstname, lastname) = form['username'].value, form['password'].value, form['firstname'].value, form['lastname'].value

			con = sqlite3.connect('users.db')
			cur = con.cursor()
			cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username VARCHAR(100), password VARCHAR(100), firstname VARCHAR(100), lastname VARCHAR(100), hash VARCHAR(100))')
			con.commit()
			msg = ''
			cur.execute("SELECT rowid FROM users WHERE username = ?", (username,))
			data=cur.fetchall()
			if len(data)==0:
				msg = 'Registration successful'
				cur.execute('INSERT INTO users (id, username, password, firstname, lastname, hash) VALUES(NULL, ?, ?, ?, ?, NULL)', (username, password, firstname, lastname))
				con.commit()
			else:
				msg = 'Account already exists'
			con.close()
			self.send_response(301)
			#self.send_header('Location','/')
			self.send_header('Refresh','5; url="/"')
			self.end_headers()
			self.wfile.write(msg)
			
		elif self.path=="/login":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			for key in form:
				print("FORM: " + key + " " + form[key].value);
			#print "Your name is: %s" % form["your_name"].value
			cookieExpiration = 1 * 20 # 20 sec
			expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=cookieExpiration)
			
			self.send_response(301)
			#self.send_header('Location','/')
			self.send_header('Refresh','5; url="/"')#refresh:" . $timeout . "; url=login.php
			
			username = form['username'].value
			_password = form['password'].value
			
			con = sqlite3.connect('users.db')
			cur = con.cursor()
			cur.execute('SELECT * FROM users')
			for row in cur.fetchall():
				(id, login, password, fname, lname, hash) = row
				if username == login and _password == password:
					logged = True
					break

			if logged:
				hash1 = hashlib.sha224(form['password'].value).digest()
				hash2 = hashlib.sha224(str(datetime.datetime.now())).digest()
				# Xor
				sz = len(hashlib.sha224(form['password'].value).digest())
				hash = list()
				for i in range(sz):
					a = hash1[i].encode('hex')
					b = hash2[i].encode('hex')
					c = int(a, 16) ^ int(b, 16)
					hash.append(hex(c)[2:])
				print(''.join(x.encode('hex') for x in hash))
				hash = ''.join(hash)
				cur.execute('UPDATE users SET hash=? WHERE username=?', (hash, username))
				con.commit()
				
				self.send_header('Set-Cookie', "profile=" + username + "; expires=" + expires.strftime('%a, %d-%b-%Y %H:%M:%S GMT'))
				self.send_header('Set-Cookie', "hash=" + hash + "; expires=" + expires.strftime('%a, %d-%b-%Y %H:%M:%S GMT'))
			con.close()
			self.end_headers()
			return			
			
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ This class allows to handle requests in separated threads.
        No further content needed, don't touch this. """		

			
try:
	# Create a web server and define the handler to manage the
	# incoming request
	server = ThreadedHTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	# Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
