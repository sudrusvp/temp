import json
import urllib
import os
import os.path
import sys
import requests
from flask import render_template
from flask import request, url_for, make_response
from watson_developer_cloud import ConversationV1
from os.path import join, dirname
from flask import Flask
import datetime
from requests.auth import HTTPProxyAuth


conversation = ConversationV1(
    username='d60b49ab-90f3-498d-affc-151893688b38',
    password='G3acJswQk33v',
    version='2017-02-03')
print("inside global app")
conv_workspace_id = '6776819a-2d5d-4a60-bfb0-39ad48f1702f'

app = Flask(__name__, static_url_path='/static')


@app.route("/", methods=['GET', 'POST'])
def main_page():
	print("inside main")
	if request.method == 'GET':
		fullpath = 'static/doc/myfile-%s.txt'%datetime.datetime.now().strftime('%Y%m%d-%H%M%S%f')
		context_file=open(fullpath,'w+')
		context_file.close()
		resp=make_response(render_template("index2.html"))
		resp.set_cookie('file_name', fullpath)
		return resp
		
	elif request.method == 'POST':
		try:
			file_name=request.cookies.get('file_name')
			print(file_name)
		except:
			fullpath = 'static/doc/myfile-%s.txt'%datetime.datetime.now().strftime('%Y%m%d-%H%M%S%f')
			context_file=open(fullpath,'w+')
			context_file.close()
		data = request.form['message']
		context = {}
		if os.path.getsize(file_name) > 0:
			file = open(file_name,'r')
			context = json.loads(file.read())
			file.close()
		else:
			print('file is empty')
		
#		response = response_file.response_fun(conv_workspace_id,data,context)
		response = conversation.message(workspace_id = conv_workspace_id, message_input={'text' : data },context = context)
		print("***********"+json.dumps(response,indent=2)+"***************")
			
		
		file = open(file_name,'w+')
#		print("Writing " + str(json.dumps(response['context'])) + "to file........")
		file.write(str(json.dumps(response['context'])))
		file.close()
		
		json_data = {}
		script3 = """<html></html>"""
		url=""
		#if str(response['output']['nodes_visited'][0]) == 'customer_detail':
		try:
			if str(response['intents'][0]['intent']) == 'customer_detail':
				try:
					cust_detail = str(response['entities'][0]['value'])
					print("customer details="+cust_detail)
					url = 'https://ehnsarmecmpre01.extnet.ibm.com/api.php?query=%s'%cust_detail
				except:
					print("customer details not provided!!")
					script3 = """<html></html>"""
				
				try:
					return_val = requests.get(url,verify = False, proxies = {
							'http': '',
							'https': ''
					})
					json_data = return_val.json()
					print(json_data)
					script3 = """
					<html>
					<body><hr>
					<table border=0.2px>
					<tr>
					<th style="padding:2px;color:white;">NAME</th>
					<th style="padding:2px;color:white;">IMT</th>
					<th style="padding:2px;color:white;">COUNTRY</th>
					<th style="padding:2px;color:white;">COUNTRY_INV</th>
					<th style="padding:2px;color:white;">CUSTOMER_ID_IHD</th>
					<th style="padding:2px;color:white;">INV_SOURCE</th>
					<th style="padding:2px;color:white;">SECTOR</th>
					</tr>
					<tr>
					<td style="padding:2px;color:white;">{name}</td>
					<td style="padding:2px;color:white;">{imt}</td>
					<td style="padding:2px;color:white;">{country}</td>
					<td style="padding:2px;color:white;">{country_inv}</td>
					<td style="padding:2px;color:white;">{customer_id_ihd}</td>
					<td style="padding:2px;color:white;">{inv_source}</td>
					<td style="padding:2px;color:white;">{sector}</td>
					</tr>
					</table>
					</body>
					</html>""".format(name=str(json_data['NAME']),imt=str(json_data['IMT']),country=str(json_data['COUNTRY']),country_inv=str(json_data['COUNTRY_INV']),customer_id_ihd=str(json_data['CUSTOMER_ID_IHD']),inv_source=str(json_data['INV_SOURCE']),sector=str(json_data['SECTOR']))
					print("Connection established!!!!")
				except Exception as e:
					print("error occured!!")
					print(str(e))
		except:
			print("can not find the intent")
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
	

		response = str(response['output']['text'][0]) + script3 + script1
		print("leaving post method")
		return str(response)

if __name__ == "__main__":
	port = int(os.getenv('PORT', 5000))
	print("Starting app on port %d" % port)
	app.run(debug=True, port=port, host='0.0.0.0')
	
	

