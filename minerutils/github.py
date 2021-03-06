#!/opt/local/bin/python

from urllib.parse import urlparse
import os
import time
import requests as req
import re
import json
import datetime
import sys
import bigjson
from minerutils.auth import MinerWithAuthentication

class GitHub(MinerWithAuthentication):

	root = 'https://api.github.com/'
	paginationArg = 'per_page'

	def __init__(self, username=None, token=None):
		super(GitHub, self).__init__(username, token)

	def printConfig(self):
		print(vars(self))

	def _processResp(self, url, resp):
		if (resp is None):
			return None
		if (url.split('/')[0] == 'search'):
			return json.loads(resp.text)['items']
		else:
			return json.loads(resp.text)

	def get(self, url, params={}, headers={}, perPage=100):
		return self.genericApiCall(self.root, url, self.paginationArg, params, headers, perPage)

	def _get(self, url, params={}, headers={}):
		resp = req.get(url, auth=self.auth, params=params, headers=headers)
		if (resp.status_code == 403):
			while resp.headers['X-RateLimit-Remaining'] == '0':
				resetTime = float(resp.headers['X-RateLimit-Reset'])
				sleepTime = resetTime - time.time()
				if sleepTime > 0:
					self._printWithTimeStamp('Exhausted the API Rate Limit. Sleeping for ' + str(sleepTime) + ' seconds')
					time.sleep(sleepTime)
				resp = req.get(url, auth=self.auth, params=params, headers=headers)
			self._printWithTimeStamp("Resuming...")
		if (resp.status_code == 404):
			return None
		if (resp.status_code == 401):
			self._printWithTimeStamp('Authorization failure: Username/password authentication has been removed')
			return None
		return resp

	def _getNextURL(self, resp):
		if (resp is None):
			return None
		if (not 'Link' in resp.headers):
			return None
		linksText = resp.headers['Link']
		links = linksText.split(',')
		for link in links:
			if 'rel=\"next\"' in link:
				url = re.sub('<', '', re.sub('>', '', link.split(';')[0]))
				return url
		return None

	def getRepoRoot(self, repo):
		return self.root + repo['username'] + '/' + repo['repo']

	def getRemainingRateLimit(self):
		limit = self.get('rate_limit')
		return limit['rate']['remaining']

	def printRemainingRateLimit(self):
		self._printWithTimeStamp('Remaining api calls: ' + str(self.getRemainingRateLimit()))

	def _getTextFromJson(self, jsonDict):
		return json.dumps(jsonDict, separators=(',',':'))

	def repoExists(self, user, repo):
		resp = self._get(self.root + 'repos/' + user + '/' + repo)
		if (resp is None):
			return False
		else:
			return True
		
	def writeData(self, path, data):
		try:
			with open(path, 'w', encoding='utf8') as f:
				json.dump(data, f, ensure_ascii=False)
		except IOError:
			print("File not accessible")

	def readData(self, path):
		try:
			wrapper = None
			with open(path, 'rb') as f:
				wrapper = bigjson.load(f, 'utf8').to_python()
			return wrapper
		except FileNotFoundError:
			print("File not found")
		except IOError:
			print("File not accessible")
