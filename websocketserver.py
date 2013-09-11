#! /usr/bin/env python

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.gen
import Button
import Repository
import threading
import time

class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.render("default.html")

	def post(self):
		self.render("default.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	waiters = set()

	def open(self):
		self.set_nodelay(True)
		print('Socket Connected: ' + str(self.request.remote_ip))
		repo = Repository.Repository()
		self.write_message(str(repo.get_current_count()))
		WebSocketHandler.waiters.add(self)

	def on_close(self):
		WebSocketHandler.waiters.remove(self)

	@classmethod
	def send_updates(cls, index):
		for waiter in cls.waiters:
			try:
				waiter.write_message(index)
			except:
				print("Error sending message")

	def on_message(self, message):
		self.write_message(u"Server echoed: " + message)

application = tornado.web.Application([
	(r"/", MainHandler),
	(r'/static/(.*)', tornado.web.StaticFileHandler, {'path': '/home/pi/Projects/TheButton_WebSocket/static'}),
	(r"/(favicon\.ico)", tornado.web.StaticFileHandler, {'path': '/home/pi/Projects/TheButton_WebSocket/static'}),
	(r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler, {'path': '/home/pi/Projects/TheButton_WebSocket/static'}),
	(r"/(apple-touch-icon-precomposed\.png)", tornado.web.StaticFileHandler, {'path': '/home/pi/Projects/TheButton_WebSocket/static'}),
	(r"/websocket", WebSocketHandler),
])

def testmethod():
	index = 20
	button = Button.Button(11)
	repo = Repository.Repository()
	index = int(repo.get_current_count())
	WebSocketHandler.send_updates(str(index))
	while 1:
		if button.pressed():
			index -= 1
			if index < 0:
				index = 20
			WebSocketHandler.send_updates(str(index))
			repo.set_count(index)
		time.sleep(0.05)

if __name__ == "__main__":
	threading.Thread(target=testmethod).start()
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(80)
	tornado.ioloop.IOLoop.instance().start()