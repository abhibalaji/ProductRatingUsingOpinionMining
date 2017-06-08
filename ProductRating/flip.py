import urllib2
import urllib
import urlparse
import csv
import re
from bs4 import BeautifulSoup
 
 
class FlipkartCategory():
 
    def __init__(self,category,url):
        self.category = category
        self.url = url
        self.producttitle = []
        self.productlinks = []

    def changelink(self,url):
        productlink = urlparse.urlparse(url)
        path = productlink.path.split('/')
        path[2] = 'product-reviews'
        return productlink.scheme + "://" + productlink.hostname + '/'.join(path)
 
    def crawlproducts(self,url,start,over):
        #print start
        #if start > 40:
            # remove this if condition to crawl all laptops. 
            # This is just for testing.  
         #   print "Done"
        #  return 
        if over:
            print "Done"
            return 
        page = BeautifulSoup(urllib2.urlopen(url).read())
        products = page.find("div",{"class" : "4-per-row"})
        if products:
            links = products.findAll("a",{"class" : "fk-display-block"})
            if links:
                for l in links:
                    self.productlinks.append(self.changelink("http://www.flipkart.com"+l.get('href')))
            else:
                over = True
        start = start + 20
        url = url + "&start=" + str(start)
        self.crawlproducts(url,start,over)


    def getproductlinks(self):
        return self.productlinks
 
 
 
 
 
 
class Flipkart():
 
    def __init__(self,category,url=""):
        self.category = category
        self.url  = url
        self.productlinks = []
        self.producttitle = ''
        self.f = None
        self.writer = None
        

    def createWriter(self,filename): 
        self.f = open(filename,"ab")
        self.writer = csv.writer(self.f)

    def closefile(self):
        self.f.close()

    def  getproductname(self):
        # Retrieve product name from a flipkart URL
        product = urlparse.urlparse(self.url)
        return product.path.split('/')[1]
 
    def crawl(self,url,start,over):
        # Get stars, title, review,helpful,veriified from a given base URL. 
        #Automatically crawls next page until there are no more reviews
        # url - Product Reviews url page
        # start - starting value for the review (similar to page number)
        # over - Boolean value to indicate whether all reviews are extracted or not. If True
         
         if over:
            print "Done"
            return
         page = urllib2.urlopen(url)
         print page.getcode()
         if page.getcode() == 200:
             reviewpage = BeautifulSoup(urllib2.urlopen(url).read())
             reviews = reviewpage.findAll("div",{"class" : "fk-review"})
             if reviews:
                 self.producttitle = reviewpage.find("h1",{"class" : "title"}).text.split('Reviews of')[1]
                 try:
                     for r in reviews:
                         stars  = (r.find("div",{"class": "fk-stars"}).get('title'))
                         title = r.find("strong").text.strip()
                         review = unicode(r.find("span",{"class" : "review-text"}).text.strip().replace('\n',' '))
                         helpful = r.findAll("div",{"class" : "unit"})[-2].text.strip()
                         if r.find("div",{"class" : "badge-certified-buyer"}):
                              verified =u"Verified Purchase"
                         else:
                              verified = u""
                         self.writer.writerow((self.category,self.producttitle,stars,title,review,helpful,verified))
                 except UnicodeEncodeError:
                    pass


             else:
                print url
                over = True
         url = url.replace("&start="+str(start),"")
         start = start + 10
         url = url + "&start=" + str(start)

         self.crawl(url,start,over)
 
 
 
#f = Flipkart(category="Laptop Accessories",url="http://www.flipkart.com/cooler-master-notepal-l1-cooling-pad/product-reviews/ITMDYH7FZPGGUFDC?pid=ACCDYH7DHYZYDQMH&type=all")
#f.crawl(f.url,0)
 
#f = Flipkart(category="Laptop Accessories",url="http://www.flipkart.com/laptop-cooling-pad-zeb-nc4000/product-reviews/ITMD35EEUZHNRJ4D?pid=ACCD35EEGMC6QBKM&type=top")
#f.crawl(f.url,0,False)
"""
fc = FlipkartCategory(category = "Mobile Phones", url = "http://www.flipkart.com/mobiles/pr?p%5B%5D=facets.brand%255B%255D%3DMotorola&p%5B%5D=facets.brand%255B%255D%3DForme&p%5B%5D=facets.operating_system%255B%255D%3DAndroid&sid=tyy%2C4io&ref=2465a700-e83f-4606-a707-d2c30d0b748e")
fc.crawlproducts(fc.url,1,False)
 
f = Flipkart(category="Mobile Phones")
links = fc.getproductlinks()
for l in links:
    print l


for l in links[1:2]:
    f.crawl(l,0,False)
"""


f = Flipkart(category = u"Mobile Phones",url="http://www.flipkart.com/moto-g-2nd-gen/product-reviews/ITME3H4V4HKCFFCS?pid=MOBDYGZ6SHNB7RFC&type=all&start=5190")
f.createWriter("moto-g.csv")
f.crawl(f.url,5190,False)
f.closefile()
