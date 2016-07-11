This script is for making you easy to use Arachni api in python.

You can use this following way.

```
from * import arachni

client = ArachniClient()
client.target('target_url') # set target url
client.start_scan() # start scan
client.get_scans() # you can get scan ids that are requested.
client.get_report('scan_id', 'xml') # get report in several format
```
