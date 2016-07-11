import urllib
import urllib2

class ArachniClient():
   def __init__(self, arachni_url = '127.0.0.1', arachni_port = 7331):
      self.arachni_url = arachni_url

   def get_http_request(self, api_path):
      return urllib2.urlopen(self.arachni_url + api_path).read()

   def post_api(self, api_path, payload):
      options = urllib.urlencode(payload)
      request = urllib2.Request(self.arachni_url + api_path, options)
      return urllib2.urlopen(request)['body']
      
   def get_scans(self):
      return self.get_http_request('/scans')

if __name__ == '__main__':
   a = ArachniClient('http://192.168.56.51:7331')
   print a.get_scans()
