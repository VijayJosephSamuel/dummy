import requests
import json

import smtplib  
from email.message import EmailMessage

import time

from tabulate import tabulate
from pretty_html_table import build_table
import pandas as pd

def job():
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
	dist_url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/31"
	district_response = requests.get(dist_url, headers=headers)
	district_data = district_response.content.decode()
	district_data = json.loads(district_data)

	html_header = '''<p style="text-align: center;><span style="font-family: Helvetica;"><strong><span style="font-size: 26px; color: rgb(44, 130, 201);">COWIN ALERT</span></strong></span></p> '''
	html_div_open = ''' <div style= "margin: auto; width: 70%">'''
	html_div_close = '''</div>'''
	output = []
	# first_row = ['District', 'Area', 'Hospital', 'Min_Age']
	output1 = []
	counter = 1
	for district in district_data['districts']:
		district_id = district['district_id']
		main_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+str(district_id)+"&date=26-05-2021"
		main_respone = requests.get(main_url, headers=headers)
		main_data = main_respone.content.decode()
		main_data = json.loads(main_data)

		for center in main_data.keys():
		    data = main_data[center]
		    for item in data:
		        center_id = item['center_id']
		        district_name = item['district_name']
		        block_name = item['block_name']
		        name = item['name']
		        for session in item['sessions']:
		            min_age = session['min_age_limit']
		            if min_age == 18:
		                output.append([counter, district_name,block_name, name, min_age])
		                output1.append(str(counter)+". "+str(district_name)+", "+str(block_name)+", "+str(name)+", "+str(min_age))
		                counter = counter+1

	pd_df = pd.DataFrame(output, columns = ['S.no','District', 'Area', 'Hospital', 'Min_Age'])	  
	# msg_send = tabulate(output, tablefmt='html', headers = first_row)
	msg_send = build_table(pd_df, 'blue_light')

	# mailing_list = ['vijay222ms@gmail.com', 'svigneshsp98@gmail.com', 'gokul9513@gmail.com', 'eshwarnataraj98@gmail.com ']
	mailing_list = ['vijay222ms@gmail.com']


	body = "\r\n".join(output1)
	msg = EmailMessage()
	# msg.add_header('Content-Type','text/html')
	# msg.set_content(msg_sendmsg_send)

	msg['Subject'] = 'Cowin Alert - 25th May'
	msg.set_content(html_div_open+html_header+msg_send+html_div_close, subtype='html')
	# Send the message via our own SMTP server.
	for email_to in mailing_list:
		# msg['To'] = email_to
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.login("cowin.alertapp@gmail.com", "vijayapp123")
		server.send_message(msg,"cowin.alertapp@gmail.com",email_to )
		server.quit()	
		print('Successfully Sent Email to  ' + email_to)


	time.sleep(120)


if __name__ == '__main__':
	job()