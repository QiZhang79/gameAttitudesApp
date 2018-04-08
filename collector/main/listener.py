from tweepy.streaming import StreamListener
import json
import time
import socket

class listener(StreamListener):

	def __init__(self, csocket):
		self.client_socket = csocket
		#self.start_time = time.time()
		super(listener, self).__init__()

	def on_data(self, data):
		tweetdict = json.loads(data)
		try:
			username = tweetdict['user']['name'].encode('utf-8')
			text = tweetdict['text'].encode('utf-8')
			msg = text
			#print(msg)
			self.client_socket.send(msg)
		except KeyError:
			print('Error.')

		return True


	def on_error(self, status):
		print(status)
