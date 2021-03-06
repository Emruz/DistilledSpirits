#!/opt/anaconda3/bin/python
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
# 20200229    Initial Version
# 20200306    Initial release
# 20200309    changed the fiter from "instock" to "all"
# 20200311    removed fiter "Distilled Spirits" and "New / Back in stock"
# 20200314    moved from timestamp validation of new items to a list compare from file
# 20200320    moved to comparing SKUs
# 20200322    if SKU matches, need to validate if qty on hand changed before we decide if seen before
# 20200323    add name, price and fixed updates for qty changes and send on qtyThreshold, not just new
# 20200331    moved the html header and footer to a files. 
#             still need to put the refine search into a variable and feed it into the file... 
# 20200513    modified the eQty filters to support new qoh (Sp O) value from the site
#
# -----------------------------------------------------------------------------
# Imports
import os, platform, requests, time, http, json, re
from lxml import html, etree
#from pprint import pprint
from datetime import datetime, timedelta
from dateutil import tz
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# -----------------------------------------------------------------------------
# Variable Declarations
startTime = datetime.now()
timeScale = "minutes"
testSpan = 0
qtyThreshold = 5

if platform.system() == 'Windows':
    outfile = "/Users/Shahin Pirooz/Projects/DistilledSpirits/DSList.out"
    logfile = "/Users/Shahin Pirooz/Projects/DistilledSpirits/DSList.log"
    touchfile = "/Users/Shahin Pirooz/Projects/DistilledSpirits/touch.file"
    productsfile = "/Users/Shahin Pirooz/Projects/DistilledSpirits/products.out"
    headerfile1 = "/Users/Shahin Pirooz/Projects/DistilledSpirits/htmlHeaderTop.html"
    headerfile2 = "/Users/Shahin Pirooz/Projects/DistilledSpirits/htmlHeaderBottom.html"
    footerfile = "/Users/Shahin Pirooz/Projects/DistilledSpirits/htmlFooter.html"
else:
    outfile = "/Users/shahin/Projects/DistilledSpirits/DSList.out"
    logfile = "/Users/shahin/Projects/DistilledSpirits/DSList.log"
    touchfile = "/Users/shahin/Projects/DistilledSpirits/touch.file"   
    productsfile = "/Users/shahin/Projects/DistilledSpirits/products.out"
    headerfile1 = "/Users/shahin/Projects/DistilledSpirits/htmlHeaderTop.html"
    headerfile2 = "/Users/shahin/Projects/DistilledSpirits/htmlHeaderBottom.html"
    footerfile = "/Users/shahin/Projects/DistilledSpirits/htmlFooter.html"
# Touch command for the touchfile
# os.utime(touchfile, None)
    
# open the touchfile and get the list of products from the last run
output = {}
thisProducts = {}
updateProducts = {}
lastProducts = {}
with open(productsfile, 'r') as fhLastProducts:
    lastProducts = json.loads(fhLastProducts.read())

# get contents from the outfile
IF = open(outfile, 'r')
OFContent = IF.read()
IF.close()

# open the outfile for writing if need be
OF = open(outfile, 'w')
def printing(text):
    print(text)
    OF.write("{text}\n")
        
#Auto-detect zones:
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

# Convert lastRun and determine the time between runs.
lastRun = time.ctime(os.path.getmtime(touchfile))
lastRunTimestamp = datetime.strptime(lastRun, '%a %b %d %H:%M:%S %Y')
lastRunTimestamp = lastRunTimestamp - timedelta(minutes = testSpan)

# determine time since last run and convert time zone
timeSpan = startTime - lastRunTimestamp
lastRunTimestamp = lastRunTimestamp.astimezone(to_zone)

# email setup
apiKey = os.environ.get('SENDGRID_API_KEY', None)
sender = 'Shaq <shaq@emruz.com>'
receiver = ['shahinpirooz@gmail.com']
#receiver = ['shahin@pirooz.net','jpapier@wrpwealth.com','lpolanowski@yahoo.com','sjsantandrea@gmail.com','scott@stephensongroup.net','joe.dickens@k-n-j.com','eanagel@gmail.com']
receiver = ['shahin@pirooz.net','jpapier@wrpwealth.com','leo@performmedia.com','sjsantandrea@gmail.com','scott@stephensongroup.net','joe.dickens@k-n-j.com','eanagel@gmail.com']
subject = "Shaq's Distilled List - {}".format(startTime.strftime("%b %d, %Y %I:%M %p"))

# =============================================================================
# Functions
# -----------------------------------------------------------------------------
def GetDistilledList():
    with open(headerfile1, 'r') as fhHtmlHeader:
        htmlHeaderTop = fhHtmlHeader.read()
    
    with open(headerfile2, 'r') as fhHtmlHeader:
        htmlHeaderBottom = fhHtmlHeader.read()
    
    
    urls = {
        'BourbonMaltScotchAll': "https://m.klwines.com/Products?filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-all!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,27.or,48!90$eq$1$True$ff-90-1--$&limit=100&offset=0&orderBy=60%20asc,NewProductFeedDate%20desc",
        'BourbonMaltScotchInstock': "https://m.klwines.com/Products?filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-instock!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,27.or,48!90$eq$1$True$ff-90-1--$&limit=100&offset=0&orderBy=60%20asc,NewProductFeedDate%20desc",
        'BourbonMaltRyeScothAll': "https://m.klwines.com/Products?filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-all!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,27.or,45.or,48!90$eq$1$True$ff-90-1--$&orderBy=60%20asc,NewProductFeedDate%20desc",
        'BourbonMaltRyeScothInstock': "https://m.klwines.com/Products?filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-instock!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,27.or,45.or,48!90$eq$1$True$ff-90-1--$&orderBy=60%20asc,NewProductFeedDate%20desc",
        'BourbonMaltRyeScoth': "https://m.klwines.com/Products/?filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-all!28$eq$(3)$True$ff-28-(3)--$or,27.or,45.or,48&limit=50&offset=0&orderBy=60%20asc,NewProductFeedDate%20desc&searchText="
        }
    url = urls['BourbonMaltRyeScoth']

    htmlHeader = htmlHeaderTop + url + htmlHeaderBottom
    
    with open(footerfile, 'r') as fhHtmlFooter:
        htmlFooter = fhHtmlFooter.read()

    elementCount = 0
    productCount = 0
    products = ""

    # -------------------------------------------------------------------------
    page = requests.get(url)
    tree = html.fromstring(page.content)
    productList = tree.xpath('//*[@id="ProductList"]/ul//li')
    elementCount = len(productList)
    
    #print out the comparisions from this run
    #print(f'thisRun    : {startTime.strftime("%m/%d/%Y %I:%M %p")}\nlastRun    : {lastRunTimestamp.strftime("%m/%d/%Y %I:%M %p")}\n')

    #              /html/body/div[1]/div[2]/div[2]/ul/li[2]/div/div/a/p[2]    
    #    timestamp //*[@id="ProductList"]/ul/li[1]/div/div/a/p[2]
    for e in productList:
        #assume each products is new
        # e is the current element eX is the attribute of the current element
        newProduct = True
        thresholdMet = False
        
        # Product Name
        # //*[@id="ProductList"]/ul/li[2]/div/div/a/h3
        # //*[@id="ProductList"]/ul/li[1]/div/div/a/h3/text()
        # //*[@id="ProductList"]/ul/li[2]/div/div/a/h3
        eName = e.xpath('div/div/a/h3/text()')[0].strip()
        print(f'Name: {eName}')
        
        # //*[@id="ProductList"]/ul/li[2]/div/div/a/p[1]/span
        ePrice = e.xpath('div/div/a/p[1]/span/text()')[0].strip()
        if '$' in ePrice: 
            ePrice = re.split("\\$", ePrice)[1]
        else:
            ePrice = re.split("Price: ", ePrice)[1]
        print(f'Price: ${ePrice}')

        # Product Time
        eTimeRoot = e.xpath('div/div/a/p[2]')
        eTimeutc = datetime.strptime(eTimeRoot[0].text, '%m/%d/%Y %I:%M %p')
        eTimeutc = eTimeutc.replace(tzinfo=from_zone) # Tell the datetime object that it's in UTC time zone since datetime objects are 'naive' by default
        elementTimestamp = eTimeutc.astimezone(to_zone) # Convert time zone
        strElementTimestamp = elementTimestamp.strftime("%m/%d/%Y %I:%M %p")
        eTimeRoot[0].text = strElementTimestamp # see if the first element in the list is the same as the last time

        # Product SKU
        eSkuRoot = e.xpath('div/div/a/p[3]')
        eSku = str(etree.tostring(eSkuRoot[0]), 'utf-8')
        eSku = re.split("</p>", re.split("</strong>", eSku)[1])[0]
        print(f'SKU: {eSku}')

        # Product Quantity On Hand
        eQtyRoot = e.xpath('div/div/a/p[4]/span')
        eQty = str(etree.tostring(eQtyRoot[0]), 'utf-8')            
        #eQty = re.split('&#13;\n', eQty)[1].strip()
        if '\n' in eQty: eQty = re.split('\n', eQty)[1].strip()
        if '&gt; ' in eQty: eQty = re.split('&gt; ', eQty)[1].strip()
        if '&#13;' in eQty: eQty = re.split('&#13;', eQty)[0].strip()
        if 'sold' in eQty.lower(): eQty = '0'
        if 'sp' in eQty.lower(): eQty = '666'
        print(f'QoH: {eQty}')
        
        #if there's nothing on hand, skip it
        if eQty == '0': continue

        # Raw product html with updated timestamp
        eProduct = str(etree.tostring(e), 'utf-8')

        # Products that we will use to update the file db
        updateProducts[eSku] = {'name': eName, 'price': ePrice, 'qty': eQty, 'time': strElementTimestamp, 'product' : eProduct}
        
        # Check to see if we have anything to send
        for lastSku in lastProducts.keys():
            if eSku == lastSku:
                print(f"Seen before, checking quantity...")
                lastQty = lastProducts[lastSku].get('qty','0')
                #if int(eQty) > 0 and int(eQty) <= qtyThreshold and int(lastQty) > qtyThreshold:
                if int(eQty) > 0 and int(lastQty) <= 0:
                    thresholdMet = True
                newProduct = False
                break

        #if there is a new product, or we hit the threshold let's add it to thisProducts and increment the counter
        if newProduct or thresholdMet:
            thisProducts[eSku] = {'name': eName, 'price': ePrice, 'qty': eQty, 'time': strElementTimestamp, 'product': eProduct}
            productCount +=1
            print(f'{productCount} of {elementCount} added to thisProducts')
            
    # Update output first with lastProducts, then with thisProducts
    output.update(lastProducts)
    output.update(thisProducts)
        
    #if we found new products, let's build the product content for the email
    if productCount > 0: 
        outProducts = []
        for i,s in enumerate(thisProducts):
            outProducts.append(thisProducts[s]['product'])
        products = ''.join(outProducts)
        
        print(products)
    else: # if we don't have anything send, lets just update the file db
        with open(productsfile, 'w') as fhThisProducts:
            fhThisProducts.write(json.dumps(updateProducts))

    if products:
        htmlString = htmlHeader + str(products) + htmlFooter
        printing(f'thisRun    : {startTime.strftime("%m/%d/%Y %I:%M %p")}\nlastRun    : {lastRunTimestamp.strftime("%m/%d/%Y %I:%M %p")}\n')
        printing(f'Last check at {lastRun}:')
        printing(f'{productCount} out of {elementCount} products are new in the last {timeSpan.total_seconds()/60:.2f} minutes')
        printing(f'found {productCount} products to send')
        return htmlString
    else:
        #print(f"{productCount} new products in the last {timeSpan} {timeScale}")
        #print(OFContent)
        OF.write(OFContent)
        print(f'Last check at {lastRun}:')
        print(f'{productCount} out of {elementCount} products are new in the last {timeSpan.total_seconds()/60:.2f} minutes')
        print(f'nothing to send!')
        return None

# =============================================================================
# Main Function
def main():
    # -------------------------------------------------------------------------
    # Send the message via SendGrid API.
    htmlString = GetDistilledList()
    message = Mail(
        from_email=sender,
        to_emails=receiver,
        subject=subject,
        html_content=htmlString)

    if apiKey is not None and htmlString is not None:
        try:
            sg = SendGridAPIClient(api_key=apiKey)
            response = sg.send(message)
            if response.status_code == 202:
                os.utime(touchfile, None)
                with open(productsfile, 'w') as fhThisProducts:
                    # store the data as binary data stream
                    fhThisProducts.write(json.dumps(output))

            printing(f"Status Code : {response.status_code}")
            printing(f"Body        : {response.body}")
            printing(f"Headers     : {response.headers}")
        except (http.client.IncompleteRead) as e:
            page = e.partial
            printing(f"Partial page:\n{page}")
            printing(f"Error: {e}\nTraceback: {e.with_traceback(e.__traceback__)}")
        except Exception as e:
            printing(f"Something went foobar!")
            printing(f"Error: {e}\nTraceback: {e.with_traceback(e.__traceback__)}")
        #finally:
            

    else:
        if apiKey is None:
            printing("Something went foobar with the API Key!")

if __name__ == '__main__':
    main() 
    OF.close()
