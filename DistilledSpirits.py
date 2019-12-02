#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
"""
@title: DistilledSpirit.py
@credits: Shahin Pirooz
@company: Emruz
@created: Sun Dec  1 17:30:49 2019
@python: 3.7
"""
# =============================================================================
""" This module... """
# =============================================================================
# Change History
# Date        Notes
# 20191201    Initial Version
#
# -----------------------------------------------------------------------------
# Imports
import os, base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
        Mail, Attachment, FileContent, FileType,
        FileName, Disposition, ContentId)
import datetime


# -----------------------------------------------------------------------------
# Variable Declarations
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

message = Mail(
    from_email=sender,
    to_emails=receiver,
    subject=subject,
    html_content=html)

# The image file is in the same directory as the script
fp = 'E.png'
with open(fp, 'rb') as img:
    data = img.read()
    img.close()
encoded = base64.b64encode(data).decode()
attachment = Attachment()
attachment.file_content = FileContent(encoded)
attachment.file_type = FileType('application/png')
attachment.file_name = FileName('logo.png')
attachment.disposition = Disposition('attachment')
attachment.content_id = ContentId('logo')
message.attachment = attachment
#print(message)


# =============================================================================
# Functions
# -----------------------------------------------------------------------------


# =============================================================================
# Main Function
def main():
    # -------------------------------------------------------------------------
    # Send the message via SendGrid API.
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main() 
