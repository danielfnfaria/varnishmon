from flask import Flask, render_template, make_response, flash, redirect
from flask_nav import Nav
from flask_nav.elements import *
from flask_bootstrap import Bootstrap
from lib.varnish import Varnish
from lib.core import Core
from time import time
import json

def create_app():
  app = Flask(__name__)
  Bootstrap(app)
  nav = Nav()
  
  nav.register_element('top', Navbar(
    View('Overview', 'overview'),
    Subgroup(
      'Groups',
        View('List Groups','list_group'),
        View('Add Group','add_group')
    ),
    Subgroup(
      'Servers',
        View('List Servers','list_server'),
        View('Add Server','add_server')
    ),
    View('Ban', 'index'),
    View('Users', 'index'),
  ))

  nav.init_app(app)

  # init varnish
  varnish = Varnish()

  # remove this please
  core = Core('192.168.99.100', 'varnishmon', 'root', 'docker')

  # function for make response to charts
  def makeResponse(r):
    response = make_response(r)
    response.content_type = 'application/json'
    return response

  # index content
  @app.route('/')
  def index():
    return "ok"

  @app.route('/overview', methods=['GET', 'POST'])
  def overview():
    if request.method == 'GET':
      response = core.listGroup()
      servers = core.listServer(1)
      return render_template('overview.html', groups=response, servers=servers, group_id=1)
    else:
      response = core.listGroup()
      return redirect('/overview/' + request.form['group_id'])

   
  @app.route('/overview/<group_id>', methods=['GET'])
  def overview_select(group_id):
    group_list = core.listGroup()
    servers = core.listServer(group_id)
    return render_template('overview.html', groups=group_list, servers=servers, group_id=int(group_id))

  @app.route('/add_group', methods=['GET', 'POST'])
  def add_group():
    if request.method == 'GET':
      return render_template('addGroup.html')
    else:
      response = core.addGroup(request.form['name'])
      return response

  @app.route('/list_group')
  def list_group():
    response = core.listGroup()
    return render_template('listGroup.html', groups=response)

  @app.route('/add_server', methods=['GET', 'POST'])
  def add_server():
    if request.method == 'GET':
      response = core.listGroup()
      return render_template('addServer.html', groups=response)
    else:
      response = core.addServer(request.form['name'], request.form['ip'], request.form['port'], request.form['password'], request.form['group'])
      return response

  @app.route('/list_server')
  def list_server():
    response = core.listServer()
    return render_template('listServer.html', servers=response)

  #
  # response for charts data
  #
  @app.route('/live/hit/<group_id>')
  def hit(group_id):
    response = core.listServer(group_id)
    v = varnish.only_hit_or_miss('hit', servers=response)
    return makeResponse(v)

  @app.route('/live/miss/<group_id>')
  def miss(group_id):
    response = core.listServer(group_id)
    v = varnish.only_hit_or_miss('miss', servers=response)
    return makeResponse(v)

  @app.route('/live/client_req/<group_id>')
  def client_req(group_id):
    response = core.listServer(group_id)
    v = varnish.client_req(servers=response)
    return makeResponse(v)
  
  @app.route('/live/health/<group_id>')
  def health(group_id):
    response = core.listServer(group_id)
    v = varnish.health(servers=response)
    return makeResponse(v)

  return app 


if __name__ == '__main__':
  create_app().run(debug=True)
