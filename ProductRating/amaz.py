import urllib2
import urllib
from bs4 import BeautifulSoup
import urlparse

class AmazonProductCrawler():

    def __init__(self,category,url):
         self.productlinks = []
         self.producttitle = []
         self.category = category
         self.url = url

    def changelink(self,url):

        # change the display page component of url to product-reviews to get product reviews page
        productlink = urlparse.urlparse(url)
        path  = productlink.path.split('/')
        path[2] =  'product-reviews'
        return productlink.scheme + "://" + productlink.hostname + '/'.join(path) 
        
    def crawl(self):
        products  = BeautifulSoup(urllib2.urlopen(self.url).read())
        links  = products.findAll("a", {"class" : "a-link-normal s-access-detail-page a-text-normal"})
        for link in links:
            productlink = link.get('href')
            self.productlinks.append(self.changelink(productlink))
            self.producttitle.append(link.text)

    def printlinks(self):
        for each in zip(self.producttitle,self.productlinks):
            print each

a = AmazonProductCrawler("Laptops","http://www.amazon.com/s/ref=amb_link_381401962_8?ie=UTF8&brand=dell&emi=ATVPDKIKX0DER&field-availability=-1&node=565108&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-10&pf_rd_r=0D5Y58PMW8EY90ZVG6W7&pf_rd_t=101&pf_rd_p=1952898442&pf_rd_i=565108")
a.crawl()
a.printlinks()
