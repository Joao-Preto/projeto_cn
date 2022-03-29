from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

client = MongoClient('172.17.0.2:27017')
pcpartpicker_db = client['pc_part_picker_data']
pcpartpicker_col = pcpartpicker_db['pc_part_picker_data']

def get_info(sku):
    sku_query = {'sku': sku}
    part_data = pcpartpicker_col.find(sku_query)
    if part_data.count() > 0:
        return part_data[0]
    part = parse_pcpartpicker_page(sku)
    pcpartpicker_col.insert_one(part)
    return part
    
def parse_pcpartpicker_page(sku):
    url = 'pcpartpicker.com/search/?q='+sku
    
    response = requests.get(url)
    soup = BeautifulSoup(response, 'lxml')
    
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

if __name__ == '__main__':
    print(client.list_database_names())