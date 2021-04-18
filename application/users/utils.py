import os
from flask import url_for, current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_reset_email(user):
	token = user.get_reset_token()

	message = Mail(
    	from_email=os.getenv("MAIL_USERNAME"),
    	to_emails=(user.email),
    	subject="JHack Password Reset Request",
    	html_content=f"""
    		<p>
    		Dear {user.username},
    		</p>

    		<p>
			To reset your password for JHack, visit the following link:
			{url_for("users.reset_token", token=token, _external=True)}
			</p>

			<p>
			Please note that the link will expire in 30 minutes.
			</p>

			<p>
			If you did not make this request then simply ignore this email.
			</p>
		""" #_external is to get an absolute URL instead of a relative URL
    )

	try:
	    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
	    response = sg.send(message)
	    print(response.status_code)
	    print(response.body)
	    print(response.headers)
	    return True
	except Exception as e:
		print(e)
		return False