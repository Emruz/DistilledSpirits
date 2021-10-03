import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from email.mime.image import MIMEImage
import datetime

sender = 'shahin@pirooz.net'
receiver = 'shahin@emruz.com'
subject = "Shaq's Distilled List - {}".format(datetime.date.today())
html = """\
<html>
  <head></head>
    <body>
      <img src="cid:image1" alt="Logo" style="width:250px;height:50px;"><br>
       <p><h4 style="font-size:15px;">Some Text.</h4></p>           
    </body>
</html>
"""
# The image file is in the same directory as the script
fp = open('logo.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

msgImage.add_header('Content-ID', '<image1>')

message = Mail(
    from_email=sender,
    to_emails=receiver,
    subject=subject,
    html_content=html,
    attachment=msgImage)

print(message)
# Send the message via SendGrid API.
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)