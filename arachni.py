import urllib2
import json

class ArachniClient(object):

   default_options = {
                       "url" : None,
                       "http" : {
                         "user_agent" : "Arachni/v2.0dev",
                         "request_timeout" : 10000,
                         "request_redirect_limit" : 5,
                         "request_concurrency" : 20,
                         "request_queue_size" : 100,
                         "request_headers" : {},
                         "response_max_size" : 500000,
                         "cookies" : {}
                       },
                       "audit" : {
                         "parameter_values" : True,
                         "exclude_vector_patterns" : [],
                         "include_vector_patterns" : [],
                         "link_templates" : []
                       },
                       "input" : {
                         "values" : {},
                         "default_values" : {
                           "(?i-mx:name)" : "arachni_name",
                           "(?i-mx:user)" : "arachni_user",
                           "(?i-mx:usr)" : "arachni_user",
                           "(?i-mx:pass)" : "5543!%arachni_secret",
                           "(?i-mx:txt)" : "arachni_text",
                           "(?i-mx:num)" : "132",
                           "(?i-mx:amount)" : "100",
                           "(?i-mx:mail)" : "arachni@email.gr",
                           "(?i-mx:account)" : "12",
                           "(?i-mx:id)" : "1"
                         },
                         "without_defaults" : False,
                         "force" : False
                       },
                       "browser_cluster" : {
                         "wait_for_elements" : {},
                         "pool_size" : 6,
                         "job_timeout" : 25,
                         "worker_time_to_live" : 100,
                         "ignore_images" : False,
                         "screen_width" : 1600,
                         "screen_height" : 1200
                       },
                       "scope" : {
                         "redundant_path_patterns" : {},
                         "dom_depth_limit" : 5,
                         "exclude_path_patterns" : [],
                         "exclude_content_patterns" : [],
                         "include_path_patterns" : [],
                         "restrict_paths" : [],
                         "extend_paths" : [],
                         "url_rewrites" : {}
                       },
                       "session" : {},
                       "checks" : [],
                       "platforms" : [],
                       "plugins" : {},
                       "no_fingerprinting" : False,
                       "authorized_by" : 'null'
                     }

   def __init__(self, arachni_url = 'http://127.0.0.1:7331'):
      self.arachni_url = arachni_url

   def get_http_request(self, api_path):
      return urllib2.urlopen(self.arachni_url + api_path).read()

   def post_api(self, api_path):
      options = json.dumps(ArachniClient.default_options)
      request = urllib2.Request(self.arachni_url + api_path, options)
      request.add_header('Content-Type', 'application/json')
      return urllib2.urlopen(request).read()

   def put_request(self, api_path):
      request = urllib2.Request(self.arachni_url + api_path)
      request.get_method = lambda: 'PUT'
      return urllib2.urlopen(request).read()

   def delete_request(self, api_path):
      request = urllib2.Request(self.arachni_url + api_path)
      request.get_method = lambda: 'DELETE'
      return urllib2.urlopen(request).read()
      
   def get_scans(self):
      return json.loads(self.get_http_request('/scans'))

   def get_status(self, scan_id):
      return json.loads(self.get_http_request('/scans/' + scan_id))

   def pause_scan(self, scan_id):
      return self.put_request('/scans/' + scan_id + '/pause')

   def resume_scan(self, scan_id):
      return self.put_request('/scans/' + scan_id + '/resume')

   def get_report(self, scan_id, report_format = None):
      if self.get_status(scan_id)['status'] == 'done':

         if report_format == 'html':
            report_format = 'html.zip'

         if report_format in ['json', 'xml', 'yaml', 'html.zip']:
            return self.get_http_request('/scans/' + scan_id + '/report.' + report_format)
         elif report_format == None:
            return self.get_http_request('/scans/' + scan_id + '/report')
         else:
            print 'your requested format is not available.'

      else:
         print 'your requested scan is in progress.'

   def delete_scan(self, scan_id):
      return self.delete_request('/scans/' + scan_id)

   def start_scan(self):
      if ArachniClient.default_options['url']:
         return json.loads(self.post_api('/scans'))
      else:
         print 'Target is not set!'

   def target(self, target_url):
      try:
         urllib2.urlopen(target_url)
      except HTTPError, e:
         print e.code
         return
      ArachniClient.default_options['url'] = target_url

if __name__ == '__main__':
   a = ArachniClient()
   a.target('http://127.0.0.1:8080')
   print a.start_scan()
