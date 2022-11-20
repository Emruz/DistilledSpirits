import sys  
from PyQt5.QtGui import *  
from PyQt5.QtCore import *  
from PyQt5.QtWebEngineWidgets import *  
from lxml import html 

#Take this class for granted.Just use result of rendering.
class Render(QWebEnginePage):  
  def __init__(self, url):  
    self.app = QGuiApplication(sys.argv)  
    QWebEnginePage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.frame.load(QUrl(url))  
    self.app.exec_()  

  def _loadFinished(self, result):  
    self.frame = self.frame()  
    self.app.quit()  

url = 'https://www.klwines.com/Products?&filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-all!27&limit=50&offset=0&orderBy=60%20asc,NewProductFeedDate%20desc&searchText='  

r = Render(url)  
result = r.frame.toHtml()
# This step is important.Converting QString to Ascii for lxml to process

# The following returns an lxml element tree
archive_links = html.fromstring(str(result.toAscii()))
print(archive_links)

# The following returns an array containing the URLs
raw_links = archive_links.xpath('//*[@id="page-content"]/div[2]/div[2]/div[3]/div/table/tbody')
print(raw_links)