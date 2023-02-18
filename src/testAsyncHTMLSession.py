from requests_html import AsyncHTMLSession, HTMLSession
session = AsyncHTMLSession ()
url1='https://www.klwines.com/Products?&filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-all!27&limit=50&offset=0&orderBy=60%20asc,NewProductFeedDate%20desc&searchText='
url2='https://www.klwines.com/cdn-cgi/apps/head/hfPIcxkCxiwaX9ryqV3drUoMa4I.js'
url3='https://www.klwines.com/bundles/js?v=0hxxk59yaoQHUgQM4NnFNTFKuBAwL6QZ8DNmJZAjhVw1'
url4='https://cdn.klwines.com/javascript/amplitude-snippet-9-27-2021.js'
r1 = session.get(url1)
r2 = session.get(url2)
r3 = session.get(url3)
r4 = session.get(url4)
p1 = r1.result()
print(p1.content)
