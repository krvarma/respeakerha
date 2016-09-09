import json
import uuid
import wave
import io
from urllib import urlencode
from urllib2 import Request, urlopen, URLError, HTTPError

class WaitTimeoutError(Exception): pass
class RequestError(Exception): pass
class UnknownValueError(Exception): pass

class Apiai():
	def __init__(self, token):
		self.access_token = token
	
	def recognize(self, text, session_id = None, show_all = False):
		assert isinstance(self.access_token, str), "`username` must be a string"
		assert session_id is None or (isinstance(session_id, str) and len(session_id) <= 36), "`session_id` must be a string of up to 36 characters"

		url = "https://api.api.ai/v1/query"


		if session_id is None: session_id = uuid.uuid4().hex
		data = json.dumps({
			"query": text,
			"sessionId": session_id,
			"lang": 'en' 
		})

		request = Request(url, data = data, headers = {
			"Authorization": "Bearer {0}".format(self.access_token),
			"Content-Type": "application/json"
		})
		try:
			response = urlopen(request)
		except HTTPError as e:
			raise RequestError("recognition request failed: {0}".format(e.reason))
		except URLError as e:
			raise RequestError("recognition connection failed: {0}".format(e.reason))
			
		response_text = response.read().decode("utf-8")
		result = json.loads(response_text)

		# return results
		return result
		
# result = recognize("turn on bedroom light")

# print(result)
# print("")
# print(result["result"]["metadata"]["intentName"])
# print(result["result"]["parameters"]["room"])
# print(result["result"]["parameters"]["op"])