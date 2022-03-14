import time
from bs4 import BeautifulSoup
from flask import session
import requests
import json

chiptec_components = 'https://www.chiptec.net/componentes-para-computadores#/componentes-para-computadores?limit=24'
globaldata_components = 'https://www.globaldata.pt/componentes'
pcdiga_components = 'https://www.pcdiga.com/componentes/'
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
        
    with open('test5.json', 'w') as f:
        f.write(str(spec_list))
        
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
    

def parse_golbaldata_page(url='https://www.globaldata.pt/processador-intel-core-i3-10100f-4-core-36ghz-43ghz-6mb-skt1200-bx8070110100f'):
    http = requests.get(url, headers=globaldata_headers, allow_redirects=False)
    print(http)
    soup = BeautifulSoup(http.text, 'lxml')
    
    product = {}
    product['sku'] = soup.find('div', class_='ck-product-sku-ean-warranty-info__item').text.split()[1]
    product['price'] = soup.find('span', class_='price__amount').text.replace(' €', '').replace('\n', '')
    
    print(product)
    
    return product
   
if __name__ == '__main__':
    session = requests.Session()
    response = session.get(pcdiga_components, headers=pcdiga_headers)
    print(response)