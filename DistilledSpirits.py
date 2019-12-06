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
import os, requests, datetime
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# -----------------------------------------------------------------------------
# Variable Declarations
sender = 'Shaq <shahin@pirooz.net>'
receiver = ['shahin@emruz.com','scott@stephensongroup.net']
subject = "Shaq's Distilled List - {}".format(datetime.date.today())
url = "https://www.klwines.com/Products?&filters=sv2_dflt-stock-instock!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,9.or,24.or,27.or,48!90$eq$1$True$ff-90-1--$or,61$eq$1$True$ff-61-1--$&orderBy=60%20asc,search.score()%20desc"
apiKey = os.environ.get('SENDGRID_API_KEY', None)

# =============================================================================
# Functions
# -----------------------------------------------------------------------------
def GetDistilledList():
    request = requests.get(url)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    element = soup.find("div", {"class": "results-block clearfix"})
    
    htmlHeader = """\
    <html lang="en">
       <head>
          <meta charset="UTF-8">
        <base href="https://www.klwines.com/" target="_blank">
           <title>K&L's Distilled Spirits List</title>
       </head>
       <body>
    """
    
    htmlFooter = """\
    
    </body>
    </html>
    
    """

    # -------------------------------------------------------------------------
    # div = "<div class="results-block clearfix">"
    request = requests.get(url)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    element = soup.find("div", {"class": "results-block clearfix"})

    html = htmlHeader + str(element) + htmlFooter
    return html


# =============================================================================
# Main Function
def main():
    # -------------------------------------------------------------------------
    # Send the message via SendGrid API.
    html = GetDistilledList()
    message = Mail(
        from_email=sender,
        to_emails=receiver,
        subject=subject,
        html_content=html)

    if apiKey is not None:
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)
    else:
        print(f'The Sendgrid API key is: {apiKey}')

if __name__ == '__main__':
    main() 
