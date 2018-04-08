import tweepy
import json
from listener import listener
import socket
import requests
import time

class tweet_collector(object):

    def __init__(self, auth_file_name):
        # Load the given args
        self._auth_file_name = auth_file_name

    ####### proprty auth_file_name #######
    @property
    def auth_file_name(self):
        return self._auth_file_name

    @auth_file_name.setter
    def auth_file_name(self, value):
        try:
            open(value)
        except:
            raise Exception("Cannt open given auth_file_name.")
        self._auth_file_name = value
    ####### proprty auth_file_name #######


    def run(self):
        # Authentificate twitter api account
        self.auth_twitter()
        # Set up the connection &get the client socket
        csocket = self.set_socket()
        # Start streaming the tweets
        self.stream_tweet(csocket)


    def auth_twitter(self):
        with open(self.auth_file_name) as auth_file:
            auth_data = json.load(auth_file)
            # Get the json fields
            consumer_key = auth_data["consumer_key"]
            consumer_secret = auth_data["consumer_secret"]
            access_token_key = auth_data["access_token_key"]
            access_token_secret = auth_data["access_token_secret"]

            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token_key, access_token_secret)


    def set_socket(self):
        # Create a TCP/IP socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Get local machine name
        host = socket.gethostbyname(socket.gethostname())
        #host = '192.168.1.4'
    	#host = socket.gethostname()
        print('>>> Host Name:\t%s' % str(host))
    	# Reserve a hst for your service
        port = 5555
        server_addr = (host, port)
    	# Bind the socket with the server address
        s.bind(server_addr)
        print('>>> Listening on port:\t%s' % str(port))
    	# Calling listen() puts the socket into server mode
        s.listen(5)
        print('>>> Waiting for client connection')
    	# accept() waits for an incoming connection
    	# Establish connection with client
        client_socket, addr = s.accept()
        print('>>> Received request from ' + str(addr))
        return client_socket


    def stream_tweet(self, csocket):
        api = tweepy.API(self.auth)
        try:
            url = "http://api:5000/keyword"
            response = requests.get(url)
            keyword = response.json()['keyword']
        except:
            keyword = "OMG"
        # Instantiate the tweet listener
        t_listener = listener(csocket)
        myStream = tweepy.Stream(auth = api.auth, listener=t_listener)
        myStream.filter(track=[keyword], languages=['en'], async=True)
        '''time.sleep(30)

        #myStream.disconnect()

        while True:

            try:
                url = "http://api:5000/keyword"
                response = requests.get(url)
                new_keyword = response.json()['keyword']
            except:
                new_keyword = "OMG"

            if new_keyword != keyword:
                keyword = new_keyword
                if myStream.running is True:
                    myStream.disconnect()

                myStream = tweepy.Stream(auth = api.auth, listener=t_listener)
                myStream.filter(track=[keyword], languages=['en'], async=True)
                print(">>> Filtering keyword: "+keyword)
            time.sleep(10) # sleep for 3 sec'''
            



if __name__ == "__main__":
    auth_file_name = './config/twitter_auth.json'
    t_collector = tweet_collector(auth_file_name)
    t_collector.run()
