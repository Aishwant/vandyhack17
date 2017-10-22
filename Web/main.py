from flask import Flask, render_template, url_for, request
#from twilio.twiml.messaging_response import MessagingResponse

import json
import numpy as np

app = Flask(__name__)


@app.route("/")
def hello():
	data = {"lat": 37.775, "lng": -56.434}
	return render_template('index.html', result=data)

@app.route("/test",methods=['POST','GET'])
def results():
	if request.method == 'POST':
		key = request.form['zipcode']
	lat = latAndLng(key)
	return render_template('test.html',zipcode=lat)

@app.route('/maps')
def maps(data=None):
	data = {"lat": 37.775, "lng": -56.434}
	return render_template('maps.html',result=data)

# @app.route('/test')
# def test(data=None):
# 	data = {"lat": 37.775, "lng": -122.434}
# 	return render_template('test.html',result=json.dumps(data))

# def latAndLng(zipcode):
# 	data = file("../Dataset/cleanedArizona.csv")
# 	data = data.read()
# 	data = data.split('\n')

# 	lat=[]
# 	dct={}

# 	for i in data:
# 		tokens = i.split(',')
# 		if(tokens[4] == zipcode):
# 			dct['lat'] = np.float32(tokens[5])
# 			dct['lng'] = np.float32(tokens[6])
# 			lat.append(dct)
# 	return lat

def latAndLng(zipcode):
	data = file("../Dataset/cleanedArizona.csv")
	data = data.read()
	data = data.split('\n')

	lat1=[]
	lng1=[]
	dct_lat={}
	dct_lng={}
	lct=[]
	a=0

	for i in data:
		tokens = i.split(',')
		if(tokens[4] == zipcode):
			lat =(tokens[5])
			lng =(tokens[6])
			try:
				dct_lat[lat]=dct_lat[lat]+1
				dct_lng[lng]=dct_lng[lng]+1
			except:
				dct_lat[lat]=1
				dct_lng[lng]=1

	for k,v in dct_lat.items():
		lat1.append(np.float32(k))
	for k,v in dct_lng.items():
		lng1.append(np.float32(k))
	if len(lat1)>1000 and len(lng1)>1000:
		for i in range(999):
			lct.append(lat1[i])
			lct.append(lng1[i+1])
	elif len(lat1)>500 and len(lng1)>500:
		for i in range(499):
			lct.append(lat1[i])
			lct.append(lng1[i+1])
	elif len(lat1)>250 and len(lng1)>250:
		for i in range(249):
			lct.append(lat1[i])
			lct.append(lng1[i+1])
	elif len(lat1)>100 and len(lng1)>100:
		for i in range(99):
			lct.append(lat1[i])
			lct.append(lng1[i+1])
	elif len(lat1)<100 and len(lng1)<100:
		for i in range(49):
			lct.append(lat1[i])
			lct.append(lng1[i+1])
	return lct
	# if len(lat)>len(lng):
	# for i in range(len(lng)):
	# 	if lat[i] in lct and lng[i] in lct:
	# 		a=a+1
	# 	else:
	# 		lct.append(np.float32(lat[i]))
	# 		lct.append(np.float32(lng[i]))
	# else:
	# 	for i in range(len(lat)):
	# 		if lat[i] in lct and lng[i] in lct:
	# 			a=a+1
	# 		else:
	# 			lct.append(np.float32(lat[i]))
	# 			lct.append(np.float32(lng[i]))
	

def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    resp.message("this is a reply")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
