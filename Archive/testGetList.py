#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
"""
@title: testGetList.py
@credits: Shahin Pirooz
@company: Emruz
@created: Mon Dec  2 16:01:13 2019
@python: 3.6
"""
# =============================================================================
""" This module... """
# =============================================================================
# Change History
# Date        Notes
# 20190312    Initial Version
#
# -----------------------------------------------------------------------------
# Imports
import requests
from bs4 import BeautifulSoup

# -----------------------------------------------------------------------------
# Variable Declarations
url = "https://www.klwines.com/Products?&filters=sv2_dflt-stock-instock!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,9.or,24.or,27.or,48!90$eq$1$True$ff-90-1--$or,61$eq$1$True$ff-61-1--$&orderBy=60%20asc,search.score()%20desc"


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



# =============================================================================
# Main Function
def main():
    # -------------------------------------------------------------------------
    # div = "<div class="results-block clearfix">"
    request = requests.get(url)
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    element = soup.find("div", {"class": "results-block clearfix"})

    html = htmlHeader + str(element) + htmlFooter
    print(html[:1000])

if __name__ == '__main__':
    main() 
