import imp
from bs4 import BeautifulSoup
import requests

pcdiga_cpu = 'https://www.pcdiga.com/componentes/processadores'
headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'#,
           #'referer' : 'https://www.pcdiga.com/componentes/processadores'
          }

def cpu_parse_chiptec(url):
    html_text = requests.get('https://www.chiptec.net/componentes-para-computadores/processadores/intel-socket-1200/intel-core-i3-10100-3-6ghz-6mb-smart-cache-box.html', headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    
    product_name = soup.find_all('div', class_='prod_tit')[0].h1.text
    product_manufacturer = soup.find_all('div', class_='prod-manufacturer')[0].p.text.split()[1]
    product_sku = soup.find_all('div', class_='sku')[0].p.text.split()[1]
    print(product_name)
    print(product_manufacturer)
    print(product_manufacturer)
    with open('test.html', "w") as f:
        f.write(f'{product_name}, {product_manufacturer}, {product_sku}')
    
    
if __name__ == '__main__':
    cpu_parse_chiptec(pcdiga_cpu+'/processadores-intel/processador-intel-core-i5-12400f-6-core-2-5ghz-c-turbo-4-4ghz-18mb-skt1700-bx8071512400f')
    