import pdb
import urllib
import socket

"""
http://maps.google.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=14&size=512x512&maptype=roadmap
&markers=color:blue|label:S|40.702147,-74.015794&markers=color:green|label:G|40.711614,-74.012318
&markers=color:red|color:red|label:C|40.718217,-73.998284&sensor=false
"""

timeout = 4
socket.setdefaulttimeout(timeout)

api_url = 'http://maps.google.com/maps/api/staticmap?center=1029+King+St+W,Toronto&zoom=14&size=100x100&maptype=roadmap&sensor=false&markers=color:red|label:X|1029+King+St+W,Toronto' 
fp = urllib.urlopen(api_url)
map = fp.read()

fo = open('/var/www/massivecoupon/media/images/map.png', 'w')
fo.write(map)
fo.close()
