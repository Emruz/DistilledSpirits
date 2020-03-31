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
# 20200229    Initial Version
# 20200306    Initial release
# 20200309    changed the fiter from "instock" to "all"
# 20200311    removed fiter "Distilled Spirits" and "New / Back in stock"
# 20200314    moved from timestamp validation of new items to a list compare from file
# 20200320    moved to comparing SKUs
# 20200322    if SKU matches, need to validate if qty on hand changed before we decide if seen before
# 20200323    add name, price and fixed updates for qty changes and send on qtyThreshold, not just new
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
else:
    outfile = "/Users/shahin/Projects/DistilledSpirits/DSList.out"
    logfile = "/Users/shahin/Projects/DistilledSpirits/DSList.log"
    touchfile = "/Users/shahin/Projects/DistilledSpirits/touch.file"   
    productsfile = "/Users/shahin/Projects/DistilledSpirits/products.out"
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
    htmlHeader = """
    <html class="ui-mobile">
	<head>
		<base href="https://m.klwines.com/Products?&amp;filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-instock!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,27.or,48!90$eq$1$True$ff-90-1--$&amp;limit=50&amp;offset=0&amp;orderBy=60%20asc,NewProductFeedDate%20desc&amp;searchText=">
			<title>Shaq's Distilled List</title>
			<meta charset="utf-8">
				<meta name="SKYPE_TOOLBAR" content="SKYPE_TOOLBAR_PARSER_COMPATIBLE">
					<meta name="viewport" content="width=device-width,initial-scale=1, maximum-scale=1">
						<link rel="icon" type="image/ico" href="https://www.klwines.com/favicon.ico">
							<link rel="apple-touch-icon" href="/Content/images/apple-touch-icon.png">
								<!--[if IE]>
								<link rel="shortcut icon" href="https://www.klwines.com/favicon.ico" type="image/vnd.microsoft.icon" />
								<![endif]-->
								<link href="/bundles/style?v=eiK3LPL8u3oE7sLDDpsFX6iT0D1HgPLC_8WnOvMoNeE1" rel="stylesheet">
									<script async="" src="//www.google-analytics.com/analytics.js"></script>
									<script src="/bundles/js?v=vT47d859AGclqrWQCKaV6xIWGmOtQh-8N62JFYeqgIg1"></script>
									<!-- Google Analytics-->
									<script type="text/javascript">
                                        (function (i, s, o, g, r, a, m) {
                                            i['GoogleAnalyticsObject'] = r; i[r] = i[r] || function () {
                                                (i[r].q = i[r].q || []).push(arguments)
                                            }, i[r].l = 1 * new Date(); a = s.createElement(o),
                                            m = s.getElementsByTagName(o)[0]; a.async = 1; a.src = g; m.parentNode.insertBefore(a, m)
                                        })(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');
                                
                                        ga('create', 'MO-1856071-4', 'auto');
                                        ga('send', 'pageview');
                                
                                    </script>
									<!-- Google Analytics-->
									<script type="text/javascript">
                                        var appInsights=window.appInsights||function(config)
                                        {
                                            function r(config){ t[config] = function(){ var i = arguments; t.queue.push(function(){ t[config].apply(t, i)})} }
                                            var t = { config:config},u=document,e=window,o='script',s=u.createElement(o),i,f;for(s.src=config.url||'//az416426.vo.msecnd.net/scripts/a/ai.0.js',u.getElementsByTagName(o)[0].parentNode.appendChild(s),t.cookie=u.cookie,t.queue=[],i=['Event','Exception','Metric','PageView','Trace','Ajax'];i.length;)r('track'+i.pop());return r('setAuthenticatedUserContext'),r('clearAuthenticatedUserContext'),config.disableExceptionTracking||(i='onerror',r('_'+i),f=e[i],e[i]=function(config, r, u, e, o) { var s = f && f(config, r, u, e, o); return s !== !0 && t['_' + i](config, r, u, e, o),s}),t
                                        }({
                                            instrumentationKey:'c0c26840-25a1-47fd-b156-41543d8b4cea'
                                        });
                                        
                                        window.appInsights=appInsights;
                                        appInsights.trackPageView();
                                    </script>
									<script src="//az416426.vo.msecnd.net/scripts/a/ai.0.js"></script>
								</head>
								<body class="ui-mobile-viewport ui-overlay-a" data-gr-c-s-loaded="true">
									<div data-role="page" data-theme="a" id="home" data-url="home" tabindex="0" class="ui-page ui-body-a ui-page-active" style="min-height: 969px;">
										<div data-role="header" data-theme="c" class="ui-header ui-bar-c" role="banner">
											<div id="Header">
														</div>
														<div id="Content" data-role="content" class="ui-content" role="main">
															<div class="searchRefinement">
																<div class="selected-refinements">
																	<a href="/Products/?&amp;filters=sv2_dflt-stock-instock!206!28$eq$(3)$True$ff-28-(3)--$or,27.or,48!90$eq$1$True$ff-90-1--$&amp;limit=50&amp;offset=0&amp;orderBy=60 asc,NewProductFeedDate desc&amp;searchText=" data-role="button" data-inline="true" data-icon="delete" data-mini="true" rel="external" title="New Product Feed" data-corners="true" data-shadow="true" data-iconshadow="true" data-wrapperels="span" data-theme="a" class="ui-btn ui-btn-up-a ui-shadow ui-btn-corner-all ui-mini ui-btn-inline ui-btn-icon-left">
																		<span class="ui-btn-inner">
																			<span class="ui-btn-text">
                                                                                New Product Feed
																				<span>&nbsp;</span>
																			</span>
																			<span class="ui-icon ui-icon-delete ui-icon-shadow">&nbsp;</span>
																		</span>
																	</a>
																	<a href="/Products/?&amp;filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-instock!28$eq$(3)$True$ff-28-(3)--$or,27.or,48!90$eq$1$True$ff-90-1--$&amp;limit=50&amp;offset=0&amp;orderBy=60 asc,NewProductFeedDate desc&amp;searchText=" data-role="button" data-inline="true" data-icon="delete" data-mini="true" rel="external" title="Distilled Spirits" data-corners="true" data-shadow="true" data-iconshadow="true" data-wrapperels="span" data-theme="a" class="ui-btn ui-btn-up-a ui-shadow ui-btn-corner-all ui-mini ui-btn-inline ui-btn-icon-left">
																		<span class="ui-btn-inner">
																			<span class="ui-btn-text">
                                                                                Distilled Spirits
																				<span>&nbsp;</span>
																			</span>
																			<span class="ui-icon ui-icon-delete ui-icon-shadow">&nbsp;</span>
																		</span>
																	</a>
																	<a href="/Products/?&amp;filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-instock!206!90$eq$1$True$ff-90-1--$&amp;limit=50&amp;offset=0&amp;orderBy=60 asc,NewProductFeedDate desc&amp;searchText=" data-role="button" data-inline="true" data-icon="delete" data-mini="true" rel="external" title="Bourbon, Malt, Scotch" data-corners="true" data-shadow="true" data-iconshadow="true" data-wrapperels="span" data-theme="a" class="ui-btn ui-btn-up-a ui-shadow ui-btn-corner-all ui-mini ui-btn-inline ui-btn-icon-left">
																		<span class="ui-btn-inner">
																			<span class="ui-btn-text">
                                                                                Bourbon, Malt, Scotch
																				<span>&nbsp;</span>
																			</span>
																			<span class="ui-icon ui-icon-delete ui-icon-shadow">&nbsp;</span>
																		</span>
																	</a>
																	<a href="/Products/?&amp;filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-instock!206!28$eq$(3)$True$ff-28-(3)--$or,27.or,48&amp;limit=50&amp;offset=0&amp;orderBy=60 asc,NewProductFeedDate desc&amp;searchText=" data-role="button" data-inline="true" data-icon="delete" data-mini="true" rel="external" title="New / Back in stock" data-corners="true" data-shadow="true" data-iconshadow="true" data-wrapperels="span" data-theme="a" class="ui-btn ui-btn-up-a ui-shadow ui-btn-corner-all ui-mini ui-btn-inline ui-btn-icon-left">
																		<span class="ui-btn-inner">
																			<span class="ui-btn-text">
                                                                                New / Back in stock
																				<span>&nbsp;</span>
																			</span>
																			<span class="ui-icon ui-icon-delete ui-icon-shadow">&nbsp;</span>
																		</span>
																	</a>
																</div>
																<script>
                                                                function productListChangeSort(select) {
                                                                    var option = $(select).find('option:selected');
                                                            
                                                                    if (option) {
                                                                        ga('send', 'event', 'Facets', 'Sort By', option.val());
                                                                        window.location.href = '/Products?' + option.attr("data-url");
                                                                    }
                                                                }
                                                                </script>
																</div>
															</div>
															<div id="ProductList" data-role="" data-inset="false" data-iconpos="right" data-collapsed="false">
    """
    
    htmlFooter = """
                                                                <script>
                                                                    function _formatAMPM(date) {
                                                                        var hours = date.getHours();
                                                                        var minutes = date.getMinutes();
                                                                        var ampm = hours >= 12 ? 'pm' : 'am';
                                                                        hours = hours % 12;
                                                                        hours = hours ? hours : 12; // the hour '0' should be '12'
                                                                        minutes = minutes < 10 ? '0' + minutes : minutes;
                                                                        var strTime = hours + ':' + minutes + ' ' + ampm;
                                                                        return strTime;
                                                                    }
                                                                
                                                                    $(document).ready(function () {
                                                                        var dateElements = document.getElementsByClassName("formatDate");
                                                                
                                                                        for (var i in dateElements) {
                                                                            try {
                                                                                var elem = dateElements[i];
                                                                                if (elem.getAttribute) {
                                                                                    var _date = new Date(elem.getAttribute("value"));
                                                                                    var date = new Date(Date.UTC(_date.getFullYear(), _date.getMonth(), _date.getDate(), _date.getHours(), _date.getMinutes(), _date.getSeconds()));
                                                                                    elem.innerHTML = date.getMonth() + 1 + "/" + date.getDate() + "/" + date.getFullYear() + " " + _formatAMPM(date);
                                                                                }
                                                                            } catch (ex) {
                                                                                console.log(ex);
                                                                            }
                                                                        }
                                                                    });
																</script>
															</div>
																			<div class="ui-loader ui-corner-all ui-body-a ui-loader-default">
																				<span class="ui-icon ui-icon-loading"></span>
																				<h1>loading</h1>
																			</div>
																			<span id="buffer-extension-hover-button" style="display: none; position: absolute; z-index: 8675309; width: 100px; height: 25px; background-image: url(&quot;chrome-extension://noojglkidnpfjbincgijbaiedldjfbhh/data/shared/img/buffer-hover-icon@1x.png&quot;); background-size: 100px 25px; opacity: 0.9; cursor: pointer;"></span>
																		</body>
																	</html>
    """

    urls = {
        'BourbonMaltScotchAll': "https://m.klwines.com/Products?filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-all!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,27.or,48!90$eq$1$True$ff-90-1--$&limit=100&offset=0&orderBy=60%20asc,NewProductFeedDate%20desc",
        'BourbonMaltScotchInstock': "https://m.klwines.com/Products?filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-instock!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,27.or,48!90$eq$1$True$ff-90-1--$&limit=100&offset=0&orderBy=60%20asc,NewProductFeedDate%20desc",
        'BourbonMaltRyeScothAll': "https://m.klwines.com/Products?filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-all!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,27.or,45.or,48!90$eq$1$True$ff-90-1--$&orderBy=60%20asc,NewProductFeedDate%20desc",
        'BourbonMaltRyeScothInstock': "https://m.klwines.com/Products?filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-instock!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,27.or,45.or,48!90$eq$1$True$ff-90-1--$&orderBy=60%20asc,NewProductFeedDate%20desc",
        'BourbonMaltRyeScoth': "https://m.klwines.com/Products/?filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-all!28$eq$(3)$True$ff-28-(3)--$or,27.or,45.or,48&limit=50&offset=0&orderBy=60%20asc,NewProductFeedDate%20desc&searchText="
        }
    url = urls['BourbonMaltRyeScoth']
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
        eQty = re.split('&#13;\n', eQty)[1].strip()
        if '&' in eQty: eQty = re.split(';', eQty)[1].strip()
        if 'sold' in eQty.lower(): eQty = '0'
        print(f'QoH: {eQty}')

        # Raw product html with updated timestamp
        eProduct = str(etree.tostring(e), 'utf-8')

        # Products that we will use to update the file db
        updateProducts[eSku] = {'name': eName, 'price': ePrice, 'qty': eQty, 'time': strElementTimestamp, 'product' : eProduct}
        
        # Check to see if we have anything to send
        for lastSku in lastProducts.keys():
            if eSku == lastSku:
                print(f"Seen before, checking quantity...")
                lastQty = lastProducts[lastSku].get('qty','0')
                if int(eQty) > 0 and int(eQty) <= qtyThreshold and int(lastQty) > qtyThreshold:
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
        products = "<ul>"
        products += ''.join(outProducts)
        products += "</ul>"
        
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
