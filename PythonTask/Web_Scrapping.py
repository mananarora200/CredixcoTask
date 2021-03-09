## Importing Libraries
import requests
import json
from bs4 import BeautifulSoup

class WebSrapper:
    ## Fetches all the data, formats it and also helps in easy access of data
    def get_data(self,url):
        r = requests.get(url)
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

if __name__ == "__main__":
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
        temp_data = scrapper.get_data(f"https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage={i+1}")
        Data.extend(temp_data)
    #Here we print all the Scrapped data from the Website
    print(Data)
    #Also write the data in json format
    with open('test.json', 'w') as f:
        json.dump(Data , f)
