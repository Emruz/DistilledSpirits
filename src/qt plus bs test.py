import bs4 as bs
import sys
import urllib.request
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl

class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def main():
    page = Page('https://www.klwines.com/Products?&filters=sv2_NewProductFeedYN$eq$1$True$ProductFeed$!dflt-stock-all!27&limit=50&offset=0&orderBy=60%20asc,NewProductFeedDate%20desc&searchText=')  
    #page = Page('https://pythonprogramming.net/parsememcparseface/')
    print(page.html)
    soup = bs.BeautifulSoup(page.html, 'html.parser')
    
    content = soup.find("div",{"class": "new-product-feed content"})
    print(content)

    
    #print(soup)
    # The following returns an array containing the URLs
    #raw_links = soup.xpath('//*[@id="page-content"]/div[2]/div[2]/div[3]/div/table/tbody')
    #print(raw_links)

if __name__ == '__main__': main()