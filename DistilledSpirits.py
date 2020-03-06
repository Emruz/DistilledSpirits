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
from lxml import html, etree
import os, requests, datetime, dateutil.parser
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# -----------------------------------------------------------------------------
# Variable Declarations
timeScale = "minutes"
timeSpan = 5
startTime = datetime.datetime.now()
lastRun  = startTime - datetime.timedelta(minutes = timeSpan)
apiKey = os.environ.get('SENDGRID_API_KEY', None)

sender = 'Shaq <shahin@pirooz.net>'
receiver = ['shahinpirooz@gmail.com']
#receiver = ['shahin@pirooz.net','jpapier@wrpwealth.com','lpolanowski@yahoo.com','sjsantandrea@gmail.com','scott@stephensongroup.net']
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

    url = "https://m.klwines.com/Products?&filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-instock!30$eq$(216)$True$ff-30-(216)--$!28$eq$(3)$True$ff-28-(3)--$or,27.or,48!90$eq$1$True$ff-90-1--$&limit=100&offset=0&orderBy=60%20asc,NewProductFeedDate%20desc&searchText="
    output = []
    productCount = 0
    products = ""
    
    # -------------------------------------------------------------------------
    page = requests.get(url)
    tree = html.fromstring(page.content)
    productList = tree.xpath('//*[@id="ProductList"]/ul//li')
   
    
    #    timestamp //*[@id="ProductList"]/ul/li[1]/div/div/a/p[2]
    #              //*[@id="ProductList"]/ul/li[2]/div/div/a/p[2]
    #              /html/body/div[1]/div[2]/div[2]/ul/li[2]/div/div/a/p[2]    
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
        products = "<ul>"
        products += ''.join(output)
        products += "</ul>"
        
        print(products)
    
    print(f"{productCount} new products in the last {timeSpan} {timeScale}")
        
    if productCount > 0:
        htmlString = htmlHeader + str(products) + htmlFooter
        return htmlString
    else:
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
