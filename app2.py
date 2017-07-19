import json
import urllib
import os
import os.path
import sys
import requests
import datetime
from flask import session
from flask import render_template
from flask import request, url_for, make_response,redirect
from watson_developer_cloud import ConversationV1
from os.path import join, dirname
from flask import Flask
from watson_developer_cloud import NaturalLanguageClassifierV1
import pysolr
from watson_developer_cloud import RetrieveAndRankV1

	
conversation = ConversationV1(
    username='8f852f62-ded3-4c89-b696-f6999670f391',
    password='wMCxakn17KSZ',
    version='2017-02-03')

natural_language_classifier = NaturalLanguageClassifierV1(
	username='fa6bffcd-ebac-4ece-8b20-9baf4c23f78d',
	password='8OmO1tBVONCP')

	
print("inside global application")

#conv_workspace_id = '72e3ba4d-5ca3-4fa4-b696-4b790d55cf5d'
conv_workspace_id = '5c2446b9-28a3-40f9-906e-b46350f494b3'

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(24)

@app.route("/")
def get():
	print("inside get")
	session['context'] = {}
	session.modified=True
	resp=make_response(render_template("index.html"))
	return resp

@app.route("/", methods=['GET','POST'])
def post(): 
	print('*******starting post method****')
	data = request.form['message']
	#with open('static/doc/training_data2.csv', 'rb') as training_data:
		#classifier = natural_language_classifier.create(training_data=training_data,name='compliancebot_training_data',language='en')
	#	classifier = natural_language_classifier.list()
	#	classifier = natural_language_classifier.classify('1c5f1ex204-nlc-39444',data)
	#	print(json.dumps(classifier, indent=2))
	context = {}
	try:
		if 'context' in session:
			context = json.loads(session['context'])
		else:
			context = {}
	except:
		print('value not in session')
	
	
	response = conversation.message(workspace_id = conv_workspace_id, message_input={'text' : data },context = context)
	print("***********"+json.dumps(response,indent=2)+"***************")
	
	if 'context' in session:
		session['context'] = json.dumps(response['context'])
	#	print(session['context'])
	
	#json_data = {}
	#script3 = """<html></html>"""
	#url=""

	""""try:
		if str(response['context']['action']) == 'cust_details_action':
			try:
				cust_detail = str(response['context']['param'])
				print("Query asked with customer ID. Customer details="+cust_detail)
				url = 'http://ehnsarmecmpre01.extnet.ibm.com/api.php?query=%s'%cust_detail
				return_val = requests.get(url,verify = False, proxies = {
							'http': '',
							'https': ''
					})
				json_data = return_val.json()
				print(json_data)
			except:
				print('connection issue!!!')
	except:
		print("cust_details_action not found!")
	"""	

#		script2 = """<html>
#			<p style='visibility:hidden;' id='context' name='context'>{code}</p>
#			</html>""".format(code=str(json.dumps(response['context'])))
	script4 = """<html></html>"""
	try:
		if response['intents'] and response['intents'][0]['confidence']:
			confidence = str(round(response['intents'][0]['confidence'] * 100))
			script4 = str("<HTML><BODY><hr style='height: 7px;border: 0;box-shadow: 0 10px 10px -10px white inset;width:270px;margin-left:0px'></body></html>I'm "  + confidence + "% certain about this answer!")
	except:
		print("confidence not exist")
		
		
	response = str(response['output']['text'][0]) + script4
	
	print("******leaving post method*********")
	return str(response)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 50000))
	app.run(debug=True, host='0.0.0.0', port=port)
	
	