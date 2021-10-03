#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lxml import html, etree
import requests, datetime, dateutil.parser

output = []
productCount = 0
timeScale = "minutes"
timeSpan = 5
startTime = datetime.datetime.now()
lastRun  = startTime - datetime.timedelta(minutes = timeSpan)

url = "https://m.klwines.com/Products?&filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-instock!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,27.or,48!90$eq$1$True$ff-90-1--$&limit=100&offset=0&orderBy=60%20asc,NewProductFeedDate%20desc&searchText="
page = requests.get(url)
tree = html.fromstring(page.content)
#print(f"{tree}")
print()

productList = tree.xpath('//*[@id="ProductList"]/ul//li')
print(productList)
print()
for e in productList:
    eTime = e.xpath('div/div/a/p[2]/text()')[0]
    #print(eTime)
    elementTimestamp = dateutil.parser.parse(eTime)
    print(f"thisRun : {startTime}\nlastRun : {lastRun}\neTime   : {elementTimestamp}")
    if elementTimestamp > lastRun:
        productCount +=1
        print(productCount)
        output.append(str(etree.tostring(e), 'utf-8'))
        
if productCount > 0:    
    content = "<ul>"
    content += ''.join(output)
    content += "</ul>"
    
    print(content)
    
print(f"{productCount} new products in the last {timeSpan} {timeScale}")
