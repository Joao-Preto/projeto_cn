from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

client = MongoClient('172.17.0.2:27017')
pcpartpicker_db = client['pc_part_picker_data']
pcpartpicker_col = pcpartpicker_db['pc_part_picker_data']

def get_info(sku):
    sku_query = {'Part #': sku}
    part_data = pcpartpicker_col.find_one(sku_query)
    if part_data:
        return part_data
    part = parse_pcpartpicker_page(sku)
    pcpartpicker_col.insert_one(part)
    return part

def get_parts(query_parameters):
    parts = pcpartpicker_col.find(query_parameters)
    part_list = []
    for part in parts:
        part_list.append(part)
    return part_list
    
def parse_pcpartpicker_page(sku):
    url = 'http://pcpartpicker.com/search/?q='+sku
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    spec_list = {}
    
    part_name = soup.find('h1', class_='pageTitle').text
    spec_list['cpu_name'] = part_name
    
    part_category = soup.find('section', class_='breadcrumb').ol.li.a.text
    spec_list['category'] = part_category
    
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
    print(get_info('100-100000065BOX'))