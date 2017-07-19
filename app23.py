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




#conversation = ConversationV1(
#    username='d60b49ab-90f3-498d-affc-151893688b38',
#    password='G3acJswQk33v',
#    version='2017-02-03')
	
conversation = ConversationV1(
    username='8f852f62-ded3-4c89-b696-f6999670f391',
    password='wMCxakn17KSZ',
    version='2017-02-03')

natural_language_classifier = NaturalLanguageClassifierV1(
	username='dfad65d0-710d-44c8-be8b-d67610fe00ef',
	password='KtxVFBD6u5Cq')

retrieve_and_rank = RetrieveAndRankV1(
	username='f7978c84-b42d-4f67-b0b7-28d6a239f8b9',
	password='sjJQGUrFpZ6X')
	
print("inside global application")

#conv_workspace_id = '72e3ba4d-5ca3-4fa4-b696-4b790d55cf5d'
conv_workspace_id = '179b88bb-055e-402e-8177-0f63b7198594'

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
	list_solr_clusters = retrieve_and_rank.list_solr_clusters()
	solr_cluster_id = str(list_solr_clusters['clusters'][0]['solr_cluster_id'])
	list_configs = retrieve_and_rank.list_configs(solr_cluster_id = solr_cluster_id)
	print(json.dumps(list_configs,indent=4))
	#solrclient = retrieve_and_rank.get_pysolr_client("sceaf14c95_4ac9_45be_a707_678e69dd8c11", "my")
	#results = solrclient.search("what is password")
	script6="""<html></html>"""
	#for result in results:
		#print(json.dumps(result, indent=2))
		#script6 = str(script6) + str(result) 
	data = request.form['message']
	with open('static/doc/training_data2.csv', 'rb') as training_data:
		#classifier = natural_language_classifier.create(training_data=training_data,name='compliancebot_training_data',language='en')
		#classifier = natural_language_classifier.list()
		#classifier = natural_language_classifier.classify('359f3fx202-nlc-117957',data)
		print(json.dumps(classifier, indent=2))
		i = 0
		j = 0
		class_name = [None] * 3
		while (j < 3):
			class_name[j] = classifier['classes'][i]['class_name']
			if class_name[j] == 'goodbye' or class_name[j] == 'emotions' or class_name[j] == 'courtesy' or class_name[j] == 'greetings' or class_name[j] == 'intro':
				i = i + 1
				continue
			j = j + 1
			i = i + 1
		print(class_name)
			
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
	
	i = 0
	example_list = [None] * 3
	while (i < 3):
		examples = conversation.list_examples(workspace_id = conv_workspace_id,intent = class_name[i])
		example_list[i] = examples['examples'][0]['text']
		i = i +1
	print(example_list)
	script5 = """<html><hr><body>
	<strong>Corresponding queries:</strong><br>
	<ul>
	<li><u>{query1}</u></li>
	<li><u>{query2}</u></li>
	<li><u>{query3}</u></li>
	</ul>
	<body><html>""".format(query1=example_list[0],query2=example_list[1],query3=example_list[2])
	
	if 'context' in session:
		session['context'] = json.dumps(response['context'])
		print(session['context'])
	
	json_data = {}
	script3 = """<html></html>"""
	url=""

	try:
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
		
	
		
		
	script1 = """<html><head><link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'>
		<script type="text/javascript">
		/*eslint-env jquery */
		function yes() {
			alert("Thank you!");
		}
		function no() {
			alert("Thank you!");
		}
		</script>
		</head>
		<body>
		<hr>
		<a href='#' class='btn btn-info btn-lg' onclick='yes()'>
       	<span class='glyphicon glyphicon-thumbs-up'></span> Yes
     	</a>
		<a href='#' class='btn btn-info btn-lg' onclick='no()'>
       	<span class='glyphicon glyphicon-thumbs-down'></span> No
    	</a>
		</body>
		</html>"""
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
		
	try:
		intent_name=response['intents'][0]['intent']
		if intent_name == 'greetings' or intent_name == 'emotions' or intent_name == 'goodbye' or intent_name == 'intro' or intent_name == 'name':
			script5 = """<html></html>"""
	except:
		print("intent is not smalltalk")
		
	try:
		response = str(response['output']['text'][0]) + script3 + script1 + script4 + script5 + script6
	except:
		response= "Could you please come again with the query or refresh the page."
	print("leaving post method*********************************************************************")
	return str(response)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 50000))
	app.run(debug=True, host='0.0.0.0', port=port)
	
	

