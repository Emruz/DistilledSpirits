#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


url = "http://sunsettheatre.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

font = soup.find("b", text="Past Movies:").find_next_sibling("font")
for event in font.find_all("b", recursive=False):
   event_date = event.previous_sibling.strip()
   event_text = event.get_text(strip=True)
   print(event_date, event_text)
