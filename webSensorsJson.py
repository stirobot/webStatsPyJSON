#Thanks for the callback code https://gist.github.com/aisipos/1094140
#TODO: 
##break this out so there is one sensor and other stuff is in different dirs?
##write other sensors
##add a function that figures out what OS is running
import os.path
import ping
import memuse
import alcoholsensor
import obddata
from functools import wraps
from flask import Flask, url_for, jsonify, redirect, request, current_app, send_from_directory

app = Flask(__name__)

global maxPing
global minPing
maxPing = 0
minPing = 100

obddata.setupOBD()

def support_jsonp(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		callback = request.args.get('callback', False)
		if callback:
			content = str(callback) + '(' + str(f(*args,**kwargs).data) + ')'
			return current_app.response_class(content,mimetype='application/javascript')
		else:
			return f(*args, **kwargs)
	return decorated_function

@app.route('/ping')
def pinginfo():
	return 'please use `host`/ping/`targetHost` to ping a specific host'

@app.route('/ping/<string:whoToPing>')
@support_jsonp
def pinger(whoToPing):
	global maxPing
	global minPing
	pingT=float(ping.pingSomeone(whoToPing))
	if (pingT > maxPing):
		maxPing = pingT
	if (pingT < minPing):
		minPing = pingT
	pingJson={"stats":[{"ping":pingT,"maxPing":maxPing,"minPing":minPing}]}
	resp = jsonify(pingJson)
	resp.status_code = 200
	return resp

@app.route('/memused')
@support_jsonp
def memav():
	memused = int(memuse.memuse())
	memJson = {"memused":memused}
	resp = jsonify(memJson)
	resp.status_code = 200
	return resp

@app.route('/alcohol')
@support_jsonp
def alc():
	alccontent = int(alcoholsensor.alcoholcontent())
	alcJson = {"alcoholppm":alccontent}
	resp = jsonify(alcJson)
	resp.status_code = 200
	return resp

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
