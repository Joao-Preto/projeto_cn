from cProfile import label
from bs4 import BeautifulSoup
import requests
import soupsieve

chiptec_components = 'https://www.chiptec.net/componentes-para-computadores#/componentes-para-computadores?limit=24'
pcdiga_cpu = 'https://www.pcdiga.com/componentes/processadores'
headers_chiptec = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
           #,'accept-language' : 'en-US,en'
           #,'referer' : 'https://www.pcdiga.com/componentes/processadores'
          }
dataset_directory = 'datasets/'

def product_parse_chiptec(url):
    html_text = requests.get(url, headers=headers_chiptec)
    soup = BeautifulSoup(html_text.text, 'lxml')
    
    product_sku = soup.find_all('div', class_='sku')[0].p.text.split()[1]
    product_price = soup.find('div', class_='price-box').span.span.text.replace(' €', '')
    
    return f'{product_sku}, {product_price}\n'

def parse_chiptec():
    html_text = requests.get(chiptec_components, headers=headers_chiptec)
    soup = BeautifulSoup(html_text.text, 'lxml')
    with open(dataset_directory+'chiptec.csv', 'w') as f:
        f.write('sku, price\n')
        parse_items_chiptec(f, soup)
        
                
def parse_items_chiptec(file, soup):
    item_list = soup.find('ul', class_='products-grid box').find_all('li', class_='item')
    for item in item_list:
        item_url = item.find('a')['href']
        try:
            file.write(product_parse_chiptec(item_url))
        except:
            print(item_url)
    last_link= soup.find('div', class_='toolbar-bottom').find('ol').find_all('li')[-1].find_all('a', class_='next')
    next_url=None
    if len(last_link) > 0:
        next_url= last_link[0]['href']
    if next_url is not None:
        newHtml = requests.get(next_url, headers=headers_chiptec)
        newSoup = BeautifulSoup(newHtml.text, 'lxml')
        parse_items_chiptec(file, newSoup)
    
    
if __name__ == '__main__':
    parse_chiptec()
    