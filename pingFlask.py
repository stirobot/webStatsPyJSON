#Thanks for the callback code https://gist.github.com/aisipos/1094140
import subprocess
import time
import json
from functools import wraps
from flask import Flask, url_for, jsonify, redirect, request, current_app

app = Flask(__name__)

global maxPing
global minPing
maxPing = 0
minPing = 100

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

def pingSomeone():
	output = subprocess.Popen(["ping.exe","-n", "1", "google.com"],stdout = subprocess.PIPE).communicate()[0]
	#print(output)
	#parse the output here
	msPos=output.find("time=")
	msEnd=output.find("ms")
	pingTime=(output[msPos+5:msEnd])
	return pingTime

@app.route('/ping')
@support_jsonp
def index():
	global maxPing
	global minPing
	pingT=int(pingSomeone())
	if (pingT > maxPing):
		maxPing = pingT
	if (pingT < minPing):
		minPing = pingT
	pingJson={"stats":[{"ping":pingT,"maxPing":maxPing,"minPing":minPing}]}
	resp = jsonify(pingJson)
	resp.status_code = 200

	return resp

if __name__ == '__main__':
    app.run(debug=True)
