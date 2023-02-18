from lxml import html, etree
import os, os.path, requests, time
from datetime import datetime, timedelta
from dateutil import tz
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



xpath to full site table:
//*[@id="content"]/div[2]/div[2]/div[3]/div/table/tbody
