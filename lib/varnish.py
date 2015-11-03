from time import time
from collections import OrderedDict
import urllib2
import json


class Varnish:

  def connect(self, option, username, password, host, port):
    auth = 'Basic ' + (username + ':' + password).encode('base64').rstrip()
    r = urllib2.Request('http://' +  host + ':' + port + '/' + option)
    r.add_header('Authorization', auth)
    data = urllib2.urlopen(r).read()
    return data

  def hit(self, servers):

    _sum_hit = []
    _sum_miss = []

    for server in servers:
      stats = self.connect('stats', 'varnish', str(server[4]), str(server[2]), str(server[3]))
      parse = json.loads(stats)
      _sum_hit.append(parse['MAIN.cache_hit']['value'])
    
    return sum(_sum_hit)

  def miss(self, servers):
    
    _sum_hit = []
    _sum_miss = []

    for server in servers:
      stats = self.connect('stats', 'varnish', str(server[4]), str(server[2]), str(server[3]))
      parse = json.loads(stats)
      _sum_miss.append(parse['MAIN.cache_miss']['value'])

    return sum(_sum_miss)

  def health(self, servers):
    
    _sum_hit = []
    _sum_miss = []

    for server in servers:
      stats = self.connect('stats', 'varnish', str(server[4]), str(server[2]), str(server[3]))
      parse = json.loads(stats)
      _sum_hit.append(parse['MAIN.cache_hit']['value'])
      _sum_miss.append(parse['MAIN.cache_miss']['value'])

    result = 100 * sum(_sum_hit) / (sum(_sum_hit) + sum(_sum_miss))
    return str(result)

  def only_hit_or_miss(self, option, servers):
    t = time() * 1000
    if option == "hit":
      data = [t, self.hit(servers)]
    else:
      data = [t, self.miss(servers)]
    return json.dumps(data)

  def client_req(self, servers):

    t = time() * 1000
    
    _sum_client_req = []

    for server in servers:
      stats = self.connect('stats', 'varnish', str(server[4]), str(server[2]), str(server[3]))
      parse = json.loads(stats)
      _sum_client_req.append(parse['MAIN.client_req']['value'])

    data = [t, sum(_sum_client_req)]
    return json.dumps(data)

