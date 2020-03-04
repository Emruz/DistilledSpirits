#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
"""
@title: DistilledSpirit.Ardbeg.py
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
receiver = ['shahinpirooz@gmail.com']
#receiver = ['shahinpirooz@gmail.com','scott@stephensongroup.net']
#receiver = ['shahin@pirooz.net','jpapier@wrpwealth.com','lpolanowski@yahoo.com','sjsantandrea@gmail.com','scott@stephensongroup.net']
subject = "Shaq's Distilled Ardbeg List - {}".format(datetime.date.today())

ardbeg1 = "https://m.klwines.com/Products?&filters=sv2_dflt-stock-instock!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,27.or,48&orderBy=60%20asc,search.score()%20desc&searchText=Ardbeg"
ardbeg2 = "https://m.klwines.com/Products?&filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-all!27&limit=50&offset=0&orderBy=60%20asc,NewProductFeedDate%20desc&searchText=ardbeg"
apiKey = os.environ.get('SENDGRID_API_KEY', None)
url = ardbeg1

# =============================================================================
# Functions
# -----------------------------------------------------------------------------
def GetDistilledList():    
    htmlHeader = """\
    <html lang="en">
       <head>
          <meta charset="UTF-8">
        <base href="https://m.klwines.com/" target="_blank">
           <title>Shaq's Distilled List</title>
       </head>
       <body>
    """
    
    htmlFooter = """\
    
    </body>
    </html>
    
    """
    content = ""
    # -------------------------------------------------------------------------
    # div = "<div class="results-block clearfix">"
    request = requests.get(url)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    element = soup.find("div", {"id": "ProductList"})

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
