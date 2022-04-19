import datetime
import json
from time import time
import requests
from bs4 import BeautifulSoup
from flask import abort, redirect, request, session
from redis import Redis
from rq import Queue

redis_conn  = Redis()
job_queue = Queue(connection=redis_conn)

request_id_count = 0
request_queue = []
request_status = {}

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
redirect = '<Response [301]>'
wait_signal = '<Response [429]>'

chiptec_component_list_url = 'https://www.chiptec.net/componentes-para-computadores#/componentes-para-computadores'
globaldata_component_list_url = 'https://www.globaldata.pt/componentes'
clickfield_component_list_url = 'https://www.clickfiel.pt/1/353/Componentes'

chiptec_service_url = ''
globaldata_service_url = ''
clickfield_service_url = ''
pcpartpicker_service_url = ''

part_stores = ['chiptec', 'globaldata', 'clickfield']

# Admin Method
def update_part_data():
    request_id_count = request_id_count + 1
    job = job_queue.enqueue(update_part_data_job)
    request_queue.append(job)
    request_status[request_id_count] = 'In Queue'
    return 'Request id: ' + str(request_id_count)

def get_request_status(request_id):
    return request_status[request_id] if request_id < request_id_count else abort(404)

# User Method
def get_part_by_sku(sku):
    part_prices = []
    for store in part_stores:
        url = redis_conn.get('sku:'+store+':'+sku)
        price = eval('parse_'+store+'_page(url)')
        part_prices.append({store: price})
    
    pcpartpicker_data = get_pcpartpicker_data(sku)
    
    return {'part_info': pcpartpicker_data, 'part_prices':part_prices}
        
def get_part_by_ean(ean):
    sku = redis_conn.get('ean:'+str(ean))
    
    part_prices = []
    for store in part_stores:
        url = redis_conn.get('sku:'+store+':'+sku)
        price = eval('parse_'+store+'_page(url)')
        part_prices.append({store: price})
    
    pcpartpicker_data = get_pcpartpicker_data(sku)
    
    return {'part_info': pcpartpicker_data, 'part_prices':part_prices}

# auxiliary methods
def update_part_data_job():
    update_chiptec_data()
    update_globaldata_data()
    update_clickfield_data()
    
def update_chiptec_data():
    # Get chiptec data
    products = []
    last_page_parsed = False
    components_page_num = 1
    while not last_page_parsed:
        response  = requests.get(chiptec_component_list_url+'?p='+str(components_page_num))
        soup = BeautifulSoup(response.text, 'lxml')
        
        item_soup_list = soup.find('ul', class_='products-grid box').find_all('li', class_='item')
        for item_soup in item_soup_list:
            item_url = item_soup.a['href']
            # try block?
            product = parse_chiptec_page(item_url)
            products.append(product)
        
        last_link = soup.find('div', class_='toolbar-bottom')
        if last_link is None:
            last_page_parsed = True
        else:
            components_page_num = components_page_num + 1
    # Send data to chiptec services
    requests.post(chiptec_service_url, data=products)

def parse_chiptec_page(url):
    response = requests.get(url, headers=headers, allow_redirects=False)
    soup = BeautifulSoup(response.text, 'lxml')
    
    product = {}
    product['sku']   = soup.find_all('div', class_='sku')[0].p.text.split()[1]
    product['price'] = soup.find('div', class_='price-box').span.span.text.replace(' €', '')
    product['timestamp'] = datetime.timestamp(datetime.now())
    
    #redis_conn.set('sku:chiptec:'+product['sku'],url)
    
    return product

def update_globaldata_data():
    # Get globaldata data
    products = []
    last_page_parsed = False
    components_page_num = 1
    while not last_page_parsed:
        try:
            response = requests.get(globaldata_component_list_url+'?page='+str(components_page_num), headers=headers, allow_redirects=False)
            soup = BeautifulSoup(response.text, 'lxml')
            
            product_wraper_soup = soup.find('div', class_='js-product-list')
            url_list = map(lambda child: 'https://www.globaldata.pt'+child.find('div', class_='col').a['href'], filter(lambda tag: tag.name == 'div',list(filter(lambda content: content != '\n', product_wraper_soup.contents))))

            for url in url_list:
                product = parse_globaldata_page(url)
                products.append(product)
        except:
            pass
        
        next_url = soup.find('a', class_='pagination__step--next')['href']
        if next_url == '#':
            last_page_parsed = True
        else:
            components_page_num = components_page_num + 1
    # Send data to clickfield services
    requests.post(globaldata_service_url, data=products)

def parse_globaldata_page(url):
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response == redirect:
        return {'url': url}
    if response == wait_signal:
        time.sleep(70)
        return parse_globaldata_page(url)
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    product = {}
    product['sku'] = soup.find('div', class_='ck-product-sku-ean-warranty-info__item').text.split()[1]
    product['ean'] = soup.find_all('div', class_='ck-product-sku-ean-warranty-info__item')[1].text.split()[1]
    product['price'] = soup.find('span', class_='price__amount').text.replace(' €', '').replace('\n', '')
    product['timestamp'] = datetime.timestamp(datetime.now())
    
    #redis_conn.set('sku:globaldata:'+product['sku'], url)
    #redis_conn.set('ean:'+product['ean'], product['sku'])
    
    return product

def update_clickfield_data():
    # Get clickfield data
    products = []
    last_page_parsed = False
    component__page_num = 1
    while not last_page_parsed:
        response = requests.get(clickfield_component_list_url+'?ordem=3&pagina='+str(component__page_num))
        soup = BeautifulSoup(response.text, 'lxml')
        
        item_url_list_soup = soup.find_all('div', class_='product-item')
        item_url_list = list(map(lambda url_soup: url_soup.div.a['href'], item_url_list_soup))
        
        for item_url in item_url_list:
            product = parse_clickfield_page(item_url)
            products.append(product)
            
        next_url = soup.find('li', class_='pagination-next').a
        if next_url is None:
            last_page_parsed = True
        else:
            component__page_num = component__page_num + 1
    # Send data to clickfield services
    request.post(clickfield_service_url, data=products)

def parse_clickfield_page(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    product = {}
    product['sku'] = soup.find('div', class_='referencia-ficha-produto').text.split()[1]
    price_div = soup.find('div', class_='price').div
    product['price'] = price_div.find('span', class_='whole').text.replace('€', '') + price_div.find('span', class_='fraction').text
    product['timestamp'] = datetime.timestamp(datetime.now())

    #redis_conn.set('sku:clickfield:'+product['sku'], url)
    
    return product

def get_store_from_url(url):
    return url.split('/')[2].split('.')[1]

def get_pcpartpicker_data(sku):
    response = requests.get(pcpartpicker_service_url, params={'sku':sku})
    return json.loads(response.json)

if __name__ == '__main__':
    update_globaldata_data()