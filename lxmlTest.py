#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lxml import html
import requests, datetime, dateutil.parser

startTime = datetime.datetime.now()
lastRun  = startTime - datetime.timedelta(minutes = 5)
output = []
url = "https://m.klwines.com/Products?&filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-instock!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,27.or,48!90$eq$1$True$ff-90-1--$&limit=100&offset=0&orderBy=60%20asc,NewProductFeedDate%20desc&searchText="
page = requests.get(url)
tree = html.fromstring(page.content)
print(f"{tree}")
print()

productList = tree.xpath('//*[@id="ProductList"]/ul//li')
print(productList)
print()
for e in productList:
    eTime = e.xpath('div/div/a/p[2]/text()')[0]
    print(eTime)
    elementTimestamp = dateutil.parser.parse(eTime)
    if elementTimestamp > lastRun:
        output.append(e)

print(output)