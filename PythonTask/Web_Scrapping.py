## Importing Libraries
import requests
import json
from bs4 import BeautifulSoup
import random

# This function return a list of proxy ips from the site 'https://free-proxy-list.net/'
def get_proxies():
    proxies_list = []
    res = requests.get('https://free-proxy-list.net/', headers={'User-Agent':'Mozilla/5.0'})
    soup = BeautifulSoup(res.content,"html.parser")
    for items in soup.select("#proxylisttable tbody tr"):
        if items.select('td')[3].get_text() == "United States":
            proxy = ':'.join([item.text for item in items.select("td")[:2]])
            proxies_list.append(proxy)
    return proxies_list

class WebSrapper:
    ## This function takes in a url to request to and proxy to use.
    #  This function returns all the data after formatting it
    def get_data(self,url,proxy):
        r = requests.get(url,proxies = proxy)
        content = r.content
        soup = BeautifulSoup(content,'html.parser')
        products = soup.find_all("div",class_="product")
        data = []
        for product in products:
            temp_dict = {}
            price = float(product.find("span",class_="price").get_text()[1:])
            title = product.find("a",class_="catalog-item-name").get_text()
            stock = False if product.find("span",class_="out-of-stock").get_text()=="Out of Stock" else True
            maftr = product.find("a",class_="catalog-item-brand").get_text()
            temp_dict["price"] = price
            temp_dict["title"] = title
            temp_dict["stock"] = stock
            temp_dict["maftr"] = maftr
            data.append(temp_dict)
        return data

#This is the driver code
if __name__ == "__main__":
    proxies = get_proxies()
    for p in proxies:
        print(f"Trying Proxy:{p}")
        proxy = {"http":"http://{p}"}
        
        try:
            ## Finding total number of pages for pagination
            url = "https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=1"
            r = requests.get(url)
            soup = BeautifulSoup(r.content,'html.parser')
            pages=soup.find("div",class_="pagination").get_text()
            max_page = max([int(i) for i in pages if i.isnumeric()])
            #Creating an object for class WebScrapper
            scrapper = WebSrapper()
            Data = []
            for i in range(max_page):
                temp_data = scrapper.get_data(f"https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage={i+1}",proxy)
                Data.extend(temp_data)
            #Here we print all the Scrapped data from the Website
            # print(Data)
            #Also write the data in json format
            with open('data.json', 'w') as f:
                json.dump(Data , f)
            print("Written data to data.json")
            break
        except:
            continue
