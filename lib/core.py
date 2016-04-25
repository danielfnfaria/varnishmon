import MySQLdb
import json
from flask import Flask, redirect

class Core:
  
  def __init__(self, db_host, db_name, db_user, db_pass):
    self.db_host = db_host
    self.db_name = db_name
    self.db_user = db_user
    self.db_pass = db_pass

  def connect(self):
    conn = MySQLdb.connect(host=self.db_host, user=self.db_user, passwd=self.db_pass, db=self.db_name)
    return conn

  def addGroup(self, name):
    conn = self.connect()
    c = conn.cursor()
    c.execute('insert into groups (name) values (%s)', [name])
    conn.commit()
    c.close()
    return redirect('registered') 

  def listGroup(self):
    conn = self.connect()
    c = conn.cursor()
    c.execute('select id,name from groups order by id')
    
    groups = []

    for group in c.fetchall():
      group = [group[0],group[1]]
      groups.append(group)
    c.close

    return groups

  def addServer(self, name, ip, port, password, group):
    conn = self.connect()
    c = conn.cursor()
    c.execute('insert into servers (name, ip, port, password, group_id) values (%s, %s, %s, %s, %s)', [name, ip, port, password, group])
    conn.commit()
    c.close()
    return redirect('registered') 


  def listServer(self, group_id = None):
    conn = self.connect()
    c = conn.cursor()

    if group_id == None:
      c.execute('select id, name, ip, port, password, group_id from servers order by id')

      servers = []

      for server in c.fetchall():
        server = [ server[0], server[1], server[2], server[3], server[4], server[5] ]
        servers.append(server)
      c.close()

      return servers

    else:

      c.execute('select id, name, ip, port, password, group_id from servers where group_id = %s order by id', [group_id])

      servers = []

      for server in c.fetchall():
        server = [ server[0], server[1], server[2], server[3], server[4], server[5] ]
        servers.append(server)
      c.close()

      return servers

  def getGroup(self, _id):
    conn = self.connect()
    c = conn.cursor()
    c.execute('select name from groups where id = %s', [_id])
    c.fetchall()
    return c




