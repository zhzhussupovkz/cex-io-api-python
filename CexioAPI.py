#
# CexioAPI class
# 
# @author zhzhussupovkz@gmail.com
# 
# The MIT License (MIT)
#
# Copyright (c) 2013 Zhussupov Zhassulan zhzhussupovkz@gmail.com
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import urllib
import urllib2
import hmac
import simplejson
import time

class CexioAPI(object):
	def __init__(self, client_id, api_key, secret):
		self.api_url = "https://cex.io/api/"
		self.client_id = client_id
		self.api_key = api_key
		self.secret = secret

	#for public requests
	def __public_request(command, args = {}):
		args = urllib.urlencode(args)
		url = self.api_url + command
		req = urllib2.Request(url, args)
		opener = urllib2.build_opener(req)
		f = opener.open(req)
		res = simplejson.load(f)
		return res

	#for private requests
	def __private_request(command, args = {}):
		nonce = str(time.time()).split('.')[0]
		message = nonce + self.client_id + self.api_key
		signature = hmac.new(self.secret, message, digestmod = hashlib.sha256).hexdigest().upper()
		args.update({'key' : self.api_key, 'nonce' : nonce, 'signature' : signature})
		args = urllib.urlencode(args)
		url = self.api_url + command
		req = urllib2.Request(url, args)
		opener = urllib2.build_opener(req)
		f = opener.open(req)
		res = simplejson.load(f)
		return res

	############### ticker ####################
	#Returns JSON dictionary:
		#last - last BTC price
		#high - last 24 hours price high
		#low - last 24 hours price low
		#volume - last 24 hours volume
		#bid - highest buy order
		#ask - lowest sell order
	def ticker():
		return self.__public_request('ticker/GHS/BTC')

	############### order_book ###############
	#Returns JSON dictionary with "bids" and "asks". 
	#Each is a list of open orders and each order is 
	#represented as a list of price and amount.
	def order_book():
		return self.__public_request('order_book/GHS/BTC')

	############### trade_history ###############
	#Returns a list of recent trades, where each trade is a JSON dictionary:
		#tid - trade id
		#amount - trade amount
		#price - price
		#date - UNIX timestamp
	def trade_history(since = 1):
		args = {'since' : since}
		return self.__public_request('trade_history/GHS/BTC', args)

	############## balance ################
	#Returns JSON dictionary:
		#available - available balance
		#orders - balance in pending orders
		#bonus - referral program bonus
	def balance():
		return self.__private_request('balance')

	############## open orders #############
	#Returns JSON list of open orders. Each order is represented as dictionary:
		#id - order id
		#time - timestamp
		#type - buy or sell
		#price - price
		#amount - amount
		#pending - pending amount (if partially executed)
	def open_orders():
		return self.__private_request('open_orders/GHS/BTC')

	############## cancel order ############
	#Returns 'true' if order has been found and canceled.
	#Params:
		#id - order ID
	def cancel_order(order_id):
		args = {'order_id' : order_id}
		return self.__private_request('cancel_order/GHS/BTC', args)

	############ place order #############
	#Returns JSON dictionary representing order:
		#id - order id
		#time - timestamp
		#type - buy or sell
		#price - price
		#amount - amount
		#pending - pending amount (if partially executed)
	#Params:
		#type - 'buy' or 'sell'
		#amount - amount
		#price - price
	def place_order(p_type = 'buy', amount = 1, price = 1):
		args = {'type' : p_type, 'amount' : amount, 'price' : price}
		return self.__private_request('place_order/GHS/BTC', args)








