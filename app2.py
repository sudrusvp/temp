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
conv_workspace_id = 'c0e7da75-b1f6-4dbd-bdee-5bc47fdc99e0'

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
	script10 = """<html></html>"""
	context = {}
	class_name = [None] * 3
	class_name_flag=False
	try:
		if 'context' in session:
			context = json.loads(session['context'])
		else:
			context = {}
	except:
		print('value not in session')
	
	
	response = conversation.message(workspace_id = conv_workspace_id, message_input={'text' : data },context = context)
	print("***********"+json.dumps(response,indent=2)+"***************")
	try:
		context1=response['context']['context1']
	except:
		print('context1 not there')
	""""cirats=1c5f1ex204-nlc-48450
	gem=359f41x201-nlc-207042
	uid=359f41x201-nlc-207041
	cwp=359f41x201-nlc-206908
	ecm=359f41x201-nlc-206907
	urt=1c5f1ex204-nlc-48304
	sterm=359f41x201-nlc-207081"""
	
	try:
		if response['intents'][0]['intent']:
			name = response['intents'][0]['intent']
			if name == 'goodbye' or name == 'courtesy' or name == 'greetings':
				print('smalltalk')
			else:
				if context1=='ecm_context_value':
					classifier = natural_language_classifier.classify('359f41x201-nlc-206907',data)
				
				if context1=='gem_context_value':
					classifier = natural_language_classifier.classify('359f41x201-nlc-207042',data)
				
				if context1=='urt_context_value':
					classifier = natural_language_classifier.classify('1c5f1ex204-nlc-48304',data)
					
				if context1=='uid_context_value':
					classifier = natural_language_classifier.classify('359f41x201-nlc-207041',data)
					
				if context1=='sterm_context_value':
					classifier = natural_language_classifier.classify('359f41x201-nlc-207081',data)
					
				if context1=='cirats_context_value':
					classifier = natural_language_classifier.classify('359f41x201-nlc-206907',data)
					
				if context1=='cwp_context_value':
					classifier = natural_language_classifier.classify('359f41x201-nlc-206908',data)
				print(json.dumps(classifier, indent=2))
				i = 0
				j = 0
				#class_name = [None] * 3
				while (j < 3):
					class_name[j] = classifier['classes'][i]['class_name']
					if class_name[j] == 'goodbye' or class_name[j] == 'emotions' or class_name[j] == 'courtesy' or class_name[j] == 'greetings' or class_name[j] == 'intro':
						i = i + 1
						continue
					j = j + 1
					i = i + 1
				class_name_flag=True
				print(class_name)
	except:
		print('intent not exist')
		
	if class_name_flag:
		example_list = [None] * 3
		i = 0
		while (i < 3):
			examples = conversation.list_examples(workspace_id = conv_workspace_id,intent = str(class_name[i]),page_limit=None, include_count=None, sort=None, cursor=None)
			example_list[i] = examples['examples'][0]['text']
			i = i +1
			print(example_list)
			
			script10 = """<html><hr><body>
			<strong>Corresponding queries:</strong><br>
			<ul>
			<li>{query1}</li>
			<li>{query2}</li>
			<li>{query3}</li>
			</ul>
			<body><html>""".format(query1=example_list[0],query2=example_list[1],query3=example_list[2])
	else:
		print('classnameflag false')

	
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
	

	response = response['output']['text'][0]+script4+script10
	
	
	print("******leaving post method*********")
	return response

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 50000))
	app.run(debug=True, host='0.0.0.0', port=port)
	
	