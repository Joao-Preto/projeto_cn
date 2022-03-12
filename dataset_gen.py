from cProfile import label
from cgi import print_arguments
import http
from pkgutil import iter_modules
from bs4 import BeautifulSoup
import requests
import soupsieve

chiptec_components = 'https://www.chiptec.net/componentes-para-computadores#/componentes-para-computadores?limit=24'
pcdiga_cpu = 'https://www.pcdiga.com/componentes/processadores'
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
        parse_items_chiptec(f, soup, 1)
        
                
def parse_items_chiptec(file, soup, pagina):
    item_num=1
    item_list = soup.find('ul', class_='products-grid box').find_all('li', class_='item')
    for item in item_list:
        print(str(pagina)+', '+str(item_num))
        item_url = item.find('a')['href']
        try:
            file.write(product_parse_chiptec(item_url))
        except:
            print(item_url)
        item_num = item_num+1
    last_link= soup.find('div', class_='toolbar-bottom').find('ol').find_all('li')[-1].find_all('a', class_='next')
    next_url=None
    if len(last_link) > 0:
        next_url= last_link[0]['href']
    if next_url is not None:
        newHtml = requests.get(next_url, headers=headers_chiptec)
        newSoup = BeautifulSoup(newHtml.text, 'lxml')
        parse_items_chiptec(file, newSoup, pagina+1)
    
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
   
if __name__ == '__main__':
    parse_chiptec()   