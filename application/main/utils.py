import os
from flask import current_app
import threading
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_confirmation_email(email):
	message = Mail(
    	from_email=os.getenv("MAIL_USERNAME"),
    	to_emails=(email),
    	subject="JHack 2021: Subscription Confirmation",
    	html_content=f"""
		Congratulations,

		You have successfully subscribed to receive emails from JHack 2021
		"""
    	)
	try:
	    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
	    response = sg.send(message)
	    print(response.status_code)
	    print(response.body)
	    print(response.headers)
	except Exception as e:
		print(e.body)

def send_email(app, subject, recipient, content):
	with app.app_context():
		message = Mail(from_email=os.getenv("MAIL_USERNAME"), to_emails=(recipient), subject=subject, html_content=content)
		try:
		    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
		    response = sg.send(message)
		    print(response.status_code)
		    print(response.body)
		    print(response.headers)
		except Exception as e:
			print(e.body)

def send_everyone_email(subject, recipients, content):
	threads = []
	for recipient in recipients:
		app = current_app._get_current_object()
		t = threading.Thread(target=send_email, args=[app, subject, recipient, content])
		t.start()
		threads.append(t)
	for thread in threads:
		thread.join()

def send_test_email(subject, content): #send a test email to myself
	message = Mail(from_email=os.getenv("MAIL_USERNAME"), to_emails=os.getenv("MAIL_USERNAME"), subject=subject, html_content=content)
	try:
	    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
	    response = sg.send(message)
	    print(response.status_code)
	    print(response.body)
	    print(response.headers)
	except Exception as e:
		print(e.body)