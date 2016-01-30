from time import time, sleep
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

    hit_first = []
    hit_current = []

    for server in servers:
      stats_first = self.connect('stats', 'varnish', str(server[4]), str(server[2]), str(server[3]))
      parse_first = json.loads(stats_first, strict=False)
      hit_first.append(parse_first['MAIN.cache_hit']['value'])

      sleep(1)
    
      stats_current = self.connect('stats', 'varnish', str(server[4]), str(server[2]), str(server[3]))
      parse_current = json.loads(stats_current, strict=False)
      hit_current.append(parse_current['MAIN.cache_hit']['value'])
    
    _sum_hit = sum(hit_current) - sum(hit_first)

    return _sum_hit

  def miss(self, servers):

    miss_first = []
    miss_current = []

    for server in servers:
      stats_first = self.connect('stats', 'varnish', str(server[4]), str(server[2]), str(server[3]))
      parse_first = json.loads(stats_first, strict=False)
      miss_first.append(parse_first['MAIN.cache_miss']['value'])

      sleep(1)
    
      stats_current = self.connect('stats', 'varnish', str(server[4]), str(server[2]), str(server[3]))
      parse_current = json.loads(stats_current, strict=False)
      miss_current.append(parse_current['MAIN.cache_miss']['value'])
    
    _sum_miss = sum(miss_current) - sum(miss_first)

    return _sum_miss

  def health(self, servers):
    
    hit_first = []
    miss_first = []
    hit_current = []
    miss_current = []

    for server in servers:
      stats_first = self.connect('stats', 'varnish', str(server[4]), str(server[2]), str(server[3]))
      parse_first = json.loads(stats_first, strict=False)
      hit_first.append(parse_first['MAIN.cache_hit']['value'])
      miss_first.append(parse_first['MAIN.cache_miss']['value'])

      sleep(1)

      stats_current = self.connect('stats', 'varnish', str(server[4]), str(server[2]), str(server[3]))
      parse_current = json.loads(stats_current, strict=False)
      hit_current.append(parse_current['MAIN.cache_hit']['value'])
      miss_current.append(parse_current['MAIN.cache_miss']['value'])

      _sum_hit = sum(hit_current) - sum(hit_first)
      
      _sum_miss = sum(miss_current) - sum(miss_first)
    
    result = 100 * _sum_hit / (_sum_hit + _sum_miss)
    
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
    
    client_req_first = []
    client_req_current = []

    for server in servers:
      stats_first = self.connect('stats', 'varnish', str(server[4]), str(server[2]), str(server[3]))
      parse_first = json.loads(stats_first, strict=False)
      client_req_first.append(parse_first['MAIN.client_req']['value'])

      sleep(1)
    
      stats_current = self.connect('stats', 'varnish', str(server[4]), str(server[2]), str(server[3]))
      parse_current = json.loads(stats_current, strict=False)
      client_req_current.append(parse_current['MAIN.client_req']['value'])
    
    _sum_client_req = sum(client_req_current) - sum(client_req_first)


    data = [t, _sum_client_req]
    return json.dumps(data)

