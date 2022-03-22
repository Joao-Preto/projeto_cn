from datetime import datetime
import time
from bs4 import BeautifulSoup
import requests
import json

chiptec_dir     = 'datasets/chiptec/'
assismatica_dir = 'datasets/assismatica/'
clickfield_dir  = 'datasets/clickfield/'
globaldata_dir  = 'datasets/globaldata/'

chiptec_components = 'https://www.chiptec.net/componentes-para-computadores#/componentes-para-computadores'
globaldata_components = 'https://www.globaldata.pt/componentes'
pcdiga_components = 'https://www.pcdiga.com/componentes/'
clickfield_components = 'https://www.clickfiel.pt/1/353/Componentes'
headers_chiptec = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
           #,'accept-language' : 'en-US,en'
           #,'referer' : 'https://www.pcdiga.com/componentes/processadores'
          }
headers_pcpartpicker = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
           ,'accept-language': 'en-US,en'
           ,'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
           ,'accept-encoding': 'gzip, deflate, br'
           ,'accept-language': 'en-US,en;q=0.9,pt;q=0.8,es;q=0.7'
           ,'cache-control': 'max-age=0'
           ,'cookie': 'xcsrftoken=WvajOor66I71EasgW5BE53IZy7hs9QblhaCAvEZ53vQQvONMZEgYP6AL5nEsbfa6; xsessionid=87vvticlztn2850eb82yraw02egpj8bs; xgdpr-consent=allow'
          }
globaldata_headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
           #,'accept-language' : 'en-US,en'
           #,'referer' : 'https://www.pcdiga.com/componentes/processadores'
          }
pcdiga_headers = {
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    ,'accept-language' : 'en-US,en;q=0.9,pt;q=0.8,es;q=0.7'
    ,'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    ,'accept-encoding' : 'gzip, deflate, br'
}

chip7_headers = {
     'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

assismatica_headers = {
     'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

clickfield_headers = {
     'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

dataset_directory = 'datasets/'
pcpartpicker_url = {
     'cpu'        : 'https://pcpartpicker.com/products/cpu/'
    ,'cooler'     : 'https://pcpartpicker.com/products/cpu-cooler/'
    ,'motherboard': 'https://pcpartpicker.com/products/motherboard/'
    ,'memory'     : 'https://pcpartpicker.com/products/memory/'
    ,'storage'    : 'https://pcpartpicker.com/products/internal-hard-drive/'
    ,'gpu'        : 'https://pcpartpicker.com/products/video-card/'
    ,'case'       : 'https://pcpartpicker.com/products/case/'
    ,'power_suply': 'https://pcpartpicker.com/products/power-supply/'
    ,'os'         : 'https://pcpartpicker.com/products/os/'
    ,'monitor'    : 'https://pcpartpicker.com/products/monitor/'
}

pcpartpicker_csv_header = {
     'cpu'        : 'cpu_name, sku, cpu_core_count, cpu_core_clock, cpu_boost_clock '
    ,'cooler'     : 'https://pcpartpicker.com/products/cpu-cooler/'
    ,'motherboard': 'https://pcpartpicker.com/products/motherboard/'
    ,'memory'     : 'https://pcpartpicker.com/products/memory/'
    ,'storage'    : 'https://pcpartpicker.com/products/internal-hard-drive/'
    ,'gpu'        : 'https://pcpartpicker.com/products/video-card/'
    ,'case'       : 'https://pcpartpicker.com/products/case/'
    ,'power_suply': 'https://pcpartpicker.com/products/power-supply/'
    ,'os'         : 'https://pcpartpicker.com/products/os/'
    ,'monitor'    : 'https://pcpartpicker.com/products/monitor/'
}

chip_7_components_urls = [
    'https://www.chip7.pt/102-motherboards',
    'https://www.chip7.pt/98-cpu',
    'https://www.chip7.pt/104-placas-graficas',
    'https://www.chip7.pt/101-memorias',
    'https://www.chip7.pt/103-placas-de-som',
    'https://www.chip7.pt/99-discos',
    'https://www.chip7.pt/114-drives',
    'https://www.chip7.pt/95-caixas',
    'https://www.chip7.pt/100-fontes-alimentacao',
]

assismatica_components_urls = [
    'https://www.assismatica.pt/pt/catalog/category/view/s/processadores/id/5283?p=',
    'https://www.assismatica.pt/pt/catalog/category/view/s/memorias-ram/id/5297/?p=',
    'https://www.assismatica.pt/pt/catalog/category/view/s/coolers-para-processador/id/5306/?p=',
    'https://www.assismatica.pt/pt/catalog/category/view/s/motherboards/id/5541/?p=',
    'https://www.assismatica.pt/pt/catalog/category/view/s/placas-graficas/id/5558/?p=',
    'https://www.assismatica.pt/pt/catalog/category/view/s/placas-de-som/id/5316/?p=',
    'https://www.assismatica.pt/pt/catalog/category/view/s/placas-diversas/id/5323/?p=',
    'https://www.assismatica.pt/pt/catalog/category/view/s/caixas/id/5310/?p=',
    'https://www.assismatica.pt/pt/catalog/category/view/s/fontes-de-alimentac-o/id/5290/?p=',
    'https://www.assismatica.pt/pt/catalog/category/view/s/ventoinhas/id/5324/?p=',
    'https://www.assismatica.pt/pt/catalog/category/view/s/drives-opticas/id/5937/?p='
]

def parse_chiptec():
    with open(dataset_directory+'chiptec.json', 'w') as f:
        item_dic = parse_items_chiptec(chiptec_components, 1)
        json_text = json.dump(item_dic, fp=f)
        
                
def parse_items_chiptec(url, pagina, list=[]):
    html = requests.get(url, headers=headers_chiptec)
    soup = BeautifulSoup(html.text, 'lxml')
    item_num=1
    item_list = soup.find('ul', class_='products-grid box').find_all('li', class_='item')
    for item in item_list:
        print(str(pagina)+', '+str(item_num))
        item_url = item.find('a')['href']
        try:
            parsed_item=product_parse_chiptec(item_url)
            print(parsed_item)
            list.append(parsed_item)
        except:
            print(item_url)
        item_num = item_num+1
        
    last_link= soup.find('div', class_='toolbar-bottom').find('ol').find_all('li')[-1].find_all('a', class_='next')
    if len(last_link) > 0:
        next_url= last_link[0]['href']
        return list+parse_items_chiptec(next_url, pagina+1, list)

    return list
    
def product_parse_chiptec(url):
    html_text = requests.get(url, headers=headers_chiptec)
    print(html_text)
    soup = BeautifulSoup(html_text.text, 'lxml')
    
    product = {}
    product['sku']   = soup.find_all('div', class_='sku')[0].p.text.split()[1]
    product['price'] = soup.find('div', class_='price-box').span.span.text.replace(' €', '')
    product['timestamp'] = datetime.timestamp(datetime.now())
    
    return product

def parse_chiptec_components():
    last_page_parsed = False
    components_index = 1
    item_index = 1
    while not last_page_parsed:
        print('component page: ' + str(components_index))
        response = requests.get(chiptec_components+'?p='+str(components_index), headers=headers_chiptec)
        print(response)
        soup = BeautifulSoup(response.text, 'lxml')
        
        item_list = soup.find('ul', class_='products-grid box').find_all('li', class_='item')
        for item in item_list:
            print('parsing item: ' + str(item_index))
            item_url = item.find('a')['href']
            parse_chiptec_page(item_url, item_index)
            item_index = item_index + 1
        
        last_link= soup.find('div', class_='toolbar-bottom').find('ol').find_all('li')[-1].find('a', class_='next')
        if last_link is None:
            last_page_parsed = True
        components_index = components_index + 1
    print(str(item_index)+' items parsed')
            
    
            
def parse_chiptec_page(url='https://www.chiptec.net/componentes-para-computadores/processadores/amd-socket-am4/amd-ryzen-5-5600g-3-9ghz-19mb-box.html', prod_num = None):
    response = requests.get(url, headers=headers_chiptec)
    print(response)
    soup = BeautifulSoup(response.text, 'lxml')
    
    product = {}
    product['sku']   = soup.find_all('div', class_='sku')[0].p.text.split()[1]
    product['price'] = soup.find('div', class_='price-box').span.span.text.replace(' €', '')
    product['timestamp'] = datetime.timestamp(datetime.now())
    
    if prod_num is None:
        print(product)
    else:
        with open(chiptec_dir+str(prod_num)+'.json','w') as f:
            json.dump(product, fp=f)
    
    return product

    
def parse_pcpartpicker_page(url='https://pcpartpicker.com/product/g94BD3/amd-ryzen-5-5600x-37-ghz-6-core-processor-100-100000065box'):
    html=requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    spec_list = {}
    part_name = soup.find('h1', class_='pageTitle').text
    spec_list['cpu_name']= part_name
    spec_soup_list = soup.find_all('div', class_='specs')[0].find_all('div', class_='group--spec')
    
    for spec_soup in spec_soup_list:
        spec_name = spec_soup.h3.text
        spec_paragraph = spec_soup.find('div', class_='group__content').p
        if spec_paragraph is None:
            l1_specs= spec_soup.find('div', class_='group__content').find_all('li')
            spec_1= l1_specs[0].text.replace('\n', '')
            spec_2= l1_specs[1].text.replace('\n', '')
            spec_list[spec_name+'_1']= spec_1
            spec_list[spec_name+'_2']= spec_2
        else:
            spec = spec_paragraph.text.replace('\n', '')
            spec_list[spec_name]= spec
        
    return spec_list

def parse_globaldata_products(url=globaldata_components):
    http_response = requests.get(url, headers=globaldata_headers, allow_redirects=False)
    soup = BeautifulSoup(http_response.text, 'lxml')
    
    page_soup = soup.find_all('li', class_='page-item pagination__item')
    page_num = int(page_soup[-2].a.text)
    
    product__info_list = []
    skiped_urls = []
    for page in range(1, page_num+1):
        page_http_response = requests.get('https://www.globaldata.pt/componentes?page='+str(page+1), headers=globaldata_headers, allow_redirects=False)
        print(page_http_response)
        page_soup = BeautifulSoup(page_http_response.text, 'lxml')
    
        product_wraper_soup = page_soup.find('div', class_='js-product-list')
        filtered_list = filter(lambda tag: tag.name == 'div',list(filter(lambda content: content != '\n', product_wraper_soup.contents)))
    
        
        child_num = 1
        for child in filtered_list:
            print(str(page)+', '+str(child_num))
            
            local_url = child.find('div', class_='col').a['href']
            part_url = 'https://www.globaldata.pt'+local_url
            
            try:
                parsed_page = parse_golbaldata_page(part_url)
                product__info_list.append(parsed_page)
            except:
                print(part_url)
                skiped_urls.append(part_url)
                
            child_num = child_num+1
            time.sleep(1)
        
        count = 1
        for url in skiped_urls:
            try:
                print('recovering product: ' + str(count))
                parsed_page = parse_golbaldata_page(url)
                product__info_list.append(parsed_page)
                count=count+1
            except:
                print(part_url)
            time.sleep(1)   
               
        print(str(count)+' products recovered!')
        
    with open(dataset_directory+'globaldata.json','w') as f:
        json.dump(product__info_list, fp=f)
    
def parse_globaldata_components():
    last_page_parsed = False
    components_index = 1
    item_index = 1
    skiped_urls = []
    while not last_page_parsed:
        print('component page: '+str(components_index))
        response = requests.get(globaldata_components+'?page='+str(components_index), headers=globaldata_headers)
        print(response)
        soup = BeautifulSoup(response.text, 'lxml')
        
        product_wraper_soup = soup.find('div', class_='js-product-list')
        url_list = map(lambda child: 'https://www.globaldata.pt'+child.find('div', class_='col').a['href'], filter(lambda tag: tag.name == 'div',list(filter(lambda content: content != '\n', product_wraper_soup.contents))))
        
        for url in url_list:
            print('parsing item:'+str(item_index))
            
            try:
                parse_golbaldata_page(url)
            except:
                print(url)
                skiped_urls.append(url)
            
            item_index = item_index+1
            time.sleep(1)
        
        next_url = soup.find('a', class_='pagination__step--next')['href']
        if next_url == '#':
            last_page_parsed = True
        else:
            components_index = components_index + 1
        
    count = 1
    for url in skiped_urls:
        try:
            print('recovering product: ' + str(count))
            parse_globaldata_page(url)
            count=count+1
        except:
            print(url)
        time.sleep(1)
    
    print(str(count)+' products recovered!')
        
                
        
def parse_globaldata_page(url='https://www.globaldata.pt/processador-intel-core-i3-10100f-4-core-36ghz-43ghz-6mb-skt1200-bx8070110100f', save=False):
    response = requests.get(url, headers=globaldata_headers, allow_redirects=False)
    print(response)
    soup = BeautifulSoup(response.text, 'lxml')
    
    product = {}
    product['sku'] = soup.find('div', class_='ck-product-sku-ean-warranty-info__item').text.split()[1]
    product['ean'] = soup.find_all('div', class_='ck-product-sku-ean-warranty-info__item')[1].text.split()[1]
    product['price'] = soup.find('span', class_='price__amount').text.replace(' €', '').replace('\n', '')
    product['timestamp'] = datetime.timestamp(datetime.now())
    
    if save:
        with open(globaldata_dir+product['ean']+'.json','w') as f:
            json.dump(product, fp=f)
    else:
        print(product)
        
    return product

def parse_chip7_components():
    components = []
    for coponent_list_page_url in chip_7_components_urls:
        response = requests.get(coponent_list_page_url, headers=chip7_headers)
        print(response)
        soup = BeautifulSoup(response.text, 'lxml')
        
        
        pass

def parse_chip7_page(url='https://www.chip7.pt/intel/97451-intel-core-i3-10105f-processador-37-ghz-6-mb-smart-cache-caixa.html'):
    response = requests.get(url, headers=chip7_headers)
    print(response)
    soup = BeautifulSoup(response.text, 'lxml')
    
    product = {}
    product['sku'] = soup.find('span', itemprop='sku').text
    product['price'] = soup.find('div', class_='price').span.text.replace(' €', '')
    product['timestamp'] = datetime.timestamp(datetime.now())
    
    with open('test9.html', 'w') as f:
        f.write(product['price'])
   
def parse_assismatica_components():
    url_list = []
    for component_list_url in assismatica_components_urls:
        next_separater_found = False
        page_index=0
        while not next_separater_found:
            response = requests.get(component_list_url+str(page_index), headers=assismatica_headers)
            print(response)
            soup = BeautifulSoup(response.text, 'lxml')
            page_index += page_index

            url_container_list = soup.find_all('div', class_='product-item-info')
            
            for url_container in url_container_list:
                if not url_container.a.has_attr('href'):
                    next_separater_found = True
                    break
                url=url_container.a['href']
                url_list.append(url)
                
    for url in url_list:
        print('retrieving: '+url)
        parse_assismatica_page(url)

def parse_assismatica_page(url='https://www.assismatica.pt/pt/catalog/product/view/id/1367117/s/bx80701g5925-intel-s1200-celeron-g5925-box-2x3-6-58w-g/category/5283/'):
    response= requests.get(url, headers=assismatica_headers)
    print(response)
    soup= BeautifulSoup(response.text, 'lxml')
    
    product = {}
    product['sku'] = soup.find('div', class_='sku').div.text
    product['ean'] = soup.find('div', class_='ean').div.text
    product['price'] = soup.find('span', class_='price-container').span.span.text.replace('\u00a0€', '')
    product['timestamp'] = datetime.timestamp(datetime.now())
    
    dir=assismatica_dir+product['ean']+'.json'
    with open(dir, 'w') as f:
        json.dump(product, fp=f)

def parse_clickfield_components():
    last_page_parsed = False
    components_index = 1
    parsed_items = 0
    while not last_page_parsed:
        print('parsing page '+str(components_index))
        response = requests.get(clickfield_components+'?ordem=3&pagina='+str(components_index), headers=clickfield_headers)
        print(response)
        soup = BeautifulSoup(response.text, 'lxml')
        item_url_list_soup = soup.find_all('div', class_='product-item')
        item_url_list = list(map(lambda url_soup: url_soup.div.a['href'], item_url_list_soup))
        for item_url in item_url_list:
            parsed_items = parsed_items + 1
            parse_clickfield_page(item_url, parsed_items)
            
        next_button_url_soup = soup.find('li', class_='pagination-next').a
        if next_button_url_soup is None:
            last_page_parsed = True
        components_index = components_index  + 1
    print(str(parsed_items)+' items parsed!')
    
def parse_clickfield_page(url='https://www.clickfiel.pt/2/9562/Processador-Intel-Core-i3-10100F-4-Core-3-6GHz', page=None):
    print('parsing item '+str(page))
    response = requests.get(url, clickfield_headers)
    print(response)
    soup = BeautifulSoup(response.text, 'lxml')
    
    product = {}
    product['sku'] = soup.find('div', class_='referencia-ficha-produto').text.split()[1]
    price_div = soup.find('div', class_='price').div
    product['price'] = price_div.find('span', class_='whole').text.replace('€', '') + price_div.find('span', class_='fraction').text
    product['timestamp'] = datetime.timestamp(datetime.now())
    
    if page is not None:
        with open(clickfield_dir+str(page)+'.json', 'w') as f:
            json.dump(product, fp=f)
    else:
        print(product)
        
if __name__ == '__main__':
    skiped = []
    with open('d') as lines:
        for line in lines:
            treated_line = line.replace('\n', '')
            try:
                parse_globaldata_page(treated_line, True)
            except:
                print(treated_line)
                time.sleep(70)
                skiped.append(treated_line)
            time.sleep(1)
    print('cleaning')
    for url in skiped:
        try:
            parse_globaldata_page(treated_line, True)
        except:
            print(treated_line)
            time.sleep(70)
        time.sleep(1)