import json
import requests
# criar query
# fazer query ao pcpartpicker
# percorrer skus
# pedir skus aos servicos de precos

chiptec_service_url = ''
globaldata_service_url = ''
clickfield_service_url = ''
pcpartpicker_service_url = ''

def get_price_from_sku(price_list, sku):
    for price in price_list:
        if price['sku'] == sku:
            return price

def get_processors(manufacturer, socket, series, min_clock_speed, max_clock_speed, ram_type, min_ram_size, max_ram_size, min_ram_speed, max_ram_speed):
    part_query = {}
    if manufacturer is not None:
        part_query['Manufacturer'] = manufacturer
    if socket is not None:
        part_query['Socket'] = socket
    if series is not None:
        part_query['Series'] = series
    if min_clock_speed is not None and max_clock_speed:
        part_query['Performance Core Clock'] = {'$in', [min_clock_speed, max_clock_speed]}
    elif min_clock_speed is not None:
        part_query['Performance Core Clock'] = {'$gt', min_clock_speed}
    elif max_clock_speed is not None:
        part_query['Performance Core Clock'] = {'$lt', max_clock_speed}
    #if ram_type is not None: ?
    #    part_query['Socket'] = socket
    if min_ram_size is not None and max_ram_size:
        part_query['Maximum Supported Memory'] = {'$in', [min_ram_size, max_ram_size]}
    elif min_ram_size is not None:
        part_query['Maximum Supported Memory'] = {'$gt', min_ram_size}
    elif max_ram_size is not None:
        part_query['Maximum Supported Memory'] = {'$lt', max_ram_size}
    #if min_ram_speed is not None and max_ram_speed:
    #    part_query['Maximum Supported Memory'] = {'$in', [min_ram_speed, max_ram_speed]}
    #elif min_ram_speed is not None:
    #    part_query['Maximum Supported Memory'] = {'$gt', min_ram_speed}
    #elif max_ram_speed is not None:
    #    part_query['Maximum Supported Memory'] = {'$lt', max_ram_speed}
    
    # Request pcpartpicker data
    pcpartpicker_response = requests.get(pcpartpicker_service_url+'/parts', params={'query_parameters':part_query})
    part_info_list = json.loads(pcpartpicker_response.json)
    
    sku_list = []
    for part_info in part_info_list:
        sku_list.append(part_info['Part #'])
    
    # Request prices from price-services
    chiptec_response = requests.get(chiptec_service_url+'/parts', params={'sku_list':sku_list})
    chiptec_prices = json.loads(chiptec_response.json)
    
    globaldata_response = requests.get(globaldata_service_url+'/parts', params={'sku_list':sku_list})
    globaldata_prices = json.loads(globaldata_response.json)
    
    clickfield_response = requests.get(clickfield_service_url+'/parts', params={'sku_list':sku_list})
    clickfield_prices = json.loads(clickfield_response.json)
    
    parts = []
    for part_info in part_info_list:
        part = {}
        part['sku'] = part_info['Part #']
        part['part_info'] = part_info
        prices = []
        prices.append({'chiptec':get_price_from_sku(chiptec_prices, part['sku'])})
        prices.append({'globaldata':get_price_from_sku(globaldata_prices, part['sku'])})
        prices.append({'clickfield':get_price_from_sku(clickfield_prices, part['sku'])})
        part['prices'] = prices

    return parts

def get_motherboards(manufacturer,cpu_manufacturer,socket,ram_type,max_ram_size,min_ram_size,max_ram_speed,min_ram_speed,PCIe_slots,PCIe_slots_type,sata_slots,sata_slots_type,m2_slots,m2_slots_type,back_panel,motherboard_form_factor,color):
    part_query = {}
    if manufacturer is not None:
        part_query['Manufacturer'] = manufacturer
    #if cpu_manufacturer is not None:
    #    part_query['Cpu_manufacturer'] = cpu_manufacturer
    if socket is not None:
        part_query['Socket'] = socket
    if ram_type is not None:
        part_query['Memory Type'] = ram_type
    #if min_ram_size is not None and max_ram_size:
    #    part_query['Maximum Supported Memory'] = {'$in', [min_ram_size, max_ram_size]}
    #elif min_ram_size is not None:
    #    part_query['Maximum Supported Memory'] = {'$gt', min_ram_size}
    #elif max_ram_size is not None:
    #    part_query['Maximum Supported Memory'] = {'$lt', max_ram_size}
    #if min_ram_speed is not None and max_ram_speed:
    #    part_query['Maximum Supported Memory Speed'] = {'$in', [min_ram_speed, max_ram_speed]}
    #elif min_ram_speed is not None:
    #    part_query['Maximum Supported Memory Speed'] = {'$gt', min_ram_speed}
    #elif max_ram_speed is not None:
    #    part_query['Maximum Supported Memory Speed'] = {'$lt', max_ram_speed}
    #if PCIe_slots is not None:
    #    part_query['PCIe_slots'] = PCIe_slots
    #if PCIe_slots_type is not None:
    #    part_query['PCIe_slots_type'] = PCIe_slots_type
    if sata_slots is not None:
        part_query['SATA 6 Gb/s'] = sata_slots
    #if sata_slots_type is not None:
    #    part_query['sata_slots_type'] = sata_slots_type
    #if m2_slots is not None:
    #    part_query['m2_slots'] = m2_slots
    #if m2_slots_type is not None:
    #    part_query['m2_slots_type'] = m2_slots_type
    #if back_panel is not None:
    #    part_query['back_panel'] = back_panel
    if motherboard_form_factor is not None:
        part_query['Form Factor'] = motherboard_form_factor
    if color is not None:
        part_query['Color'] = color;

    pcpartpicker_response = requests.get(pcpartpicker_service_url+'/parts', params={'query_parameters':part_query})
    part_info_list = json.loads(pcpartpicker_response.json)
    
    sku_list = []
    for part_info in part_info_list:
        sku_list.append(part_info['Part #'])
    
    # Request prices from price-services
    chiptec_response = requests.get(chiptec_service_url+'/parts', params={'sku_list':sku_list})
    chiptec_prices = json.loads(chiptec_response.json)
    
    globaldata_response = requests.get(globaldata_service_url+'/parts', params={'sku_list':sku_list})
    globaldata_prices = json.loads(globaldata_response.json)
    
    clickfield_response = requests.get(clickfield_service_url+'/parts', params={'sku_list':sku_list})
    clickfield_prices = json.loads(clickfield_response.json)
    
    parts = []
    for part_info in part_info_list:
        part = {}
        part['sku'] = part_info['Part #']
        part['part_info'] = part_info
        prices = []
        prices.append({'chiptec':get_price_from_sku(chiptec_prices, part['sku'])})
        prices.append({'globaldata':get_price_from_sku(globaldata_prices, part['sku'])})
        prices.append({'clickfield':get_price_from_sku(clickfield_prices, part['sku'])})
        part['prices'] = prices

    return parts

def get_memory_sticks(manufacturer, form_factor, min_ram_size, max_ram_size, min_ram_speed, max_ram_speed):
    part_query = {}
    if manufacturer is not None:
        part_query['Manufacturer'] = manufacturer
    if form_factor is not None:
        part_query['Form Factor'] = form_factor
    #if min_ram_size is not None and max_ram_size:
    #    part_query['Maximum Supported Memory'] = {'$in', [min_ram_size, max_ram_size]}
    #elif min_ram_size is not None:
    #    part_query['Maximum Supported Memory'] = {'$gt', min_ram_size}
    #elif max_ram_size is not None:
    #    part_query['Maximum Supported Memory'] = {'$lt', max_ram_size}
    if min_ram_speed is not None and max_ram_speed:
        part_query['Speed'] = {'$in', [min_ram_size, max_ram_size]}
    elif min_ram_speed is not None:
        part_query['Speed'] = {'$gt', min_ram_size}
    elif max_ram_speed is not None:
        part_query['Speed'] = {'$lt', max_ram_size}
        
    pcpartpicker_response = requests.get(pcpartpicker_service_url+'/parts', params={'query_parameters':part_query})
    part_info_list = json.loads(pcpartpicker_response.json)
    
    sku_list = []
    for part_info in part_info_list:
        sku_list.append(part_info['Part #'])
    
    # Request prices from price-services
    chiptec_response = requests.get(chiptec_service_url+'/parts', params={'sku_list':sku_list})
    chiptec_prices = json.loads(chiptec_response.json)
    
    globaldata_response = requests.get(globaldata_service_url+'/parts', params={'sku_list':sku_list})
    globaldata_prices = json.loads(globaldata_response.json)
    
    clickfield_response = requests.get(clickfield_service_url+'/parts', params={'sku_list':sku_list})
    clickfield_prices = json.loads(clickfield_response.json)
    
    parts = []
    for part_info in part_info_list:
        part = {}
        part['sku'] = part_info['Part #']
        part['part_info'] = part_info
        prices = []
        prices.append({'chiptec':get_price_from_sku(chiptec_prices, part['sku'])})
        prices.append({'globaldata':get_price_from_sku(globaldata_prices, part['sku'])})
        prices.append({'clickfield':get_price_from_sku(clickfield_prices, part['sku'])})
        part['prices'] = prices

    return parts

def get_graphics_card(manufacturer,GPU_generation,GPU_ports):
    part_query = {}
    if manufacturer is not None:
        part_query['Manufacturer'] = manufacturer
    if GPU_generation is not None:
        part_query['GPU_Generation'] = GPU_generation
    if GPU_ports is not None:
        part_query['GPU_ports'] = GPU_ports


    pcpartpicker_response = requests.get(pcpartpicker_service_url+'/parts', params={'query_parameters':part_query})
    part_info_list = json.loads(pcpartpicker_response.json)
    
    sku_list = []
    for part_info in part_info_list:
        sku_list.append(part_info['Part #'])
    
    # Request prices from price-services
    chiptec_response = requests.get(chiptec_service_url+'/parts', params={'sku_list':sku_list})
    chiptec_prices = json.loads(chiptec_response.json)
    
    globaldata_response = requests.get(globaldata_service_url+'/parts', params={'sku_list':sku_list})
    globaldata_prices = json.loads(globaldata_response.json)
    
    clickfield_response = requests.get(clickfield_service_url+'/parts', params={'sku_list':sku_list})
    clickfield_prices = json.loads(clickfield_response.json)
    
    parts = []
    for part_info in part_info_list:
        part = {}
        part['sku'] = part_info['Part #']
        part['part_info'] = part_info
        prices = []
        prices.append({'chiptec':get_price_from_sku(chiptec_prices, part['sku'])})
        prices.append({'globaldata':get_price_from_sku(globaldata_prices, part['sku'])})
        prices.append({'clickfield':get_price_from_sku(clickfield_prices, part['sku'])})
        part['prices'] = prices

    return parts

def get_storage(category, manufacturer, storing_type, capacity, interface):
    part_query = {}
    if manufacturer is not None:
        part_query['Manufacturer'] = manufacturer
    if category is not None:
        part_query['Type'] = category
    if capacity is not None:
        part_query['Capacity'] = capacity
    if storing_type is not None:
        part_query['Form Factor'] = storing_type
    if interface is not None:
        part_query['Interface'] = interface
    
    pcpartpicker_response = requests.get(pcpartpicker_service_url+'/parts', params={'query_parameters':part_query})
    part_info_list = json.loads(pcpartpicker_response.json)
    
    sku_list = []
    for part_info in part_info_list:
        sku_list.append(part_info['Part #'])
    
    # Request prices from price-services
    chiptec_response = requests.get(chiptec_service_url+'/parts', params={'sku_list':sku_list})
    chiptec_prices = json.loads(chiptec_response.json)
    
    globaldata_response = requests.get(globaldata_service_url+'/parts', params={'sku_list':sku_list})
    globaldata_prices = json.loads(globaldata_response.json)
    
    clickfield_response = requests.get(clickfield_service_url+'/parts', params={'sku_list':sku_list})
    clickfield_prices = json.loads(clickfield_response.json)
    
    parts = []
    for part_info in part_info_list:
        part = {}
        part['sku'] = part_info['Part #']
        part['part_info'] = part_info
        prices = []
        prices.append({'chiptec':get_price_from_sku(chiptec_prices, part['sku'])})
        prices.append({'globaldata':get_price_from_sku(globaldata_prices, part['sku'])})
        prices.append({'clickfield':get_price_from_sku(clickfield_prices, part['sku'])})
        part['prices'] = prices

    return parts

def get_power_supplies(manufacturer,min_wattage,max_wattage,modular,form_factor,color,fan,connectors,eficiency):
    part_query = {}
    if manufacturer is not None:
        part_query['manufacturer'] = manufacturer
    if min_wattage is not None and max_wattage:
        part_query['Maximum Wattage'] = {'$in', [min_wattage, max_wattage]}
    elif min_wattage is not None:
        part_query['Maximum Wattage'] = {'$gt', min_wattage}
    elif max_wattage is not None:
        part_query['Maximum Wattage'] = {'$lt', max_wattage}
    if modular is not None:
        part_query['modular'] = modular
    if form_factor is not None:
        part_query['form_factor'] = form_factor
    if color is not None:
        part_query['color'] = color
    #if connectors is not None:
    #    part_query['connectors'] = connectors
    if eficiency is not None:
        part_query['eficiency'] = eficiency
    
    part_query['fan'] = fan

    pcpartpicker_response = requests.get(pcpartpicker_service_url+'/parts', params={'query_parameters':part_query})
    part_info_list = json.loads(pcpartpicker_response.json)
    
    sku_list = []
    for part_info in part_info_list:
        sku_list.append(part_info['Part #'])
    
    # Request prices from price-services
    chiptec_response = requests.get(chiptec_service_url+'/parts', params={'sku_list':sku_list})
    chiptec_prices = json.loads(chiptec_response.json)
    
    globaldata_response = requests.get(globaldata_service_url+'/parts', params={'sku_list':sku_list})
    globaldata_prices = json.loads(globaldata_response.json)
    
    clickfield_response = requests.get(clickfield_service_url+'/parts', params={'sku_list':sku_list})
    clickfield_prices = json.loads(clickfield_response.json)
    
    parts = []
    for part_info in part_info_list:
        part = {}
        part['sku'] = part_info['Part #']
        part['part_info'] = part_info
        prices = []
        prices.append({'chiptec':get_price_from_sku(chiptec_prices, part['sku'])})
        prices.append({'globaldata':get_price_from_sku(globaldata_prices, part['sku'])})
        prices.append({'clickfield':get_price_from_sku(clickfield_prices, part['sku'])})
        part['prices'] = prices

    return parts



def get_fans(manufacturer, size, color, quantidade, pwm, led, connector, controler):
    part_query = {}
    if manufacturer is not None:
        part_query['Manufacturer'] = manufacturer
    if size is not None:
        part_query['Size'] = size
    if color is not None:
        part_query['Color'] = color
    if quantidade is not None:
        part_query['Quantidade'] = quantidade
    if led is not None:
        part_query['LED'] = led
    if connector is not None:
        part_query['Connector'] = connector
    if controler is not None:
        part_query['Controller'] = controler
    part_query['PWM'] = pwm
    
    
    pcpartpicker_response = requests.get(pcpartpicker_service_url+'/parts', params={'query_parameters':part_query})
    part_info_list = json.loads(pcpartpicker_response.json)
    
    sku_list = []
    for part_info in part_info_list:
        sku_list.append(part_info['Part #'])
    
    # Request prices from price-services
    chiptec_response = requests.get(chiptec_service_url+'/parts', params={'sku_list':sku_list})
    chiptec_prices = json.loads(chiptec_response.json)
    
    globaldata_response = requests.get(globaldata_service_url+'/parts', params={'sku_list':sku_list})
    globaldata_prices = json.loads(globaldata_response.json)
    
    clickfield_response = requests.get(clickfield_service_url+'/parts', params={'sku_list':sku_list})
    clickfield_prices = json.loads(clickfield_response.json)
    
    parts = []
    for part_info in part_info_list:
        part = {}
        part['sku'] = part_info['Part #']
        part['part_info'] = part_info
        prices = []
        prices.append({'chiptec':get_price_from_sku(chiptec_prices, part['sku'])})
        prices.append({'globaldata':get_price_from_sku(globaldata_prices, part['sku'])})
        prices.append({'clickfield':get_price_from_sku(clickfield_prices, part['sku'])})
        part['prices'] = prices

    return parts

def get_cases(manufacturer, case_type, motherboard_form_factor, color, side_panel_window, shroud, front_panel, min_graphics_card_length):
    part_query = {}
    if manufacturer is not None:
        part_query['Manufacturer'] = manufacturer
    if case_type is not None:
        part_query['Type'] = case_type
    if motherboard_form_factor is not None:
        part_query['Motherboard Form Factor'] = motherboard_form_factor
    if color is not None:
        part_query['Color'] = color
    if motherboard_form_factor is not None:
        part_query['Motherboard Form Factor'] = motherboard_form_factor
    if side_panel_window is not None:
        part_query['Side Panel Window'] = side_panel_window
    #if front_panel is not None:
    #    part_query['Front Panel USB'] = front_panel
    part_query['Side Panel Window'] = shroud
    
    pcpartpicker_response = requests.get(pcpartpicker_service_url+'/parts', params={'query_parameters':part_query})
    part_info_list = json.loads(pcpartpicker_response.json)
    
    sku_list = []
    for part_info in part_info_list:
        sku_list.append(part_info['Part #'])
    
    # Request prices from price-services
    chiptec_response = requests.get(chiptec_service_url+'/parts', params={'sku_list':sku_list})
    chiptec_prices = json.loads(chiptec_response.json)
    
    globaldata_response = requests.get(globaldata_service_url+'/parts', params={'sku_list':sku_list})
    globaldata_prices = json.loads(globaldata_response.json)
    
    clickfield_response = requests.get(clickfield_service_url+'/parts', params={'sku_list':sku_list})
    clickfield_prices = json.loads(clickfield_response.json)
    
    parts = []
    for part_info in part_info_list:
        part = {}
        part['sku'] = part_info['Part #']
        part['part_info'] = part_info
        prices = []
        prices.append({'chiptec':get_price_from_sku(chiptec_prices, part['sku'])})
        prices.append({'globaldata':get_price_from_sku(globaldata_prices, part['sku'])})
        prices.append({'clickfield':get_price_from_sku(clickfield_prices, part['sku'])})
        part['prices'] = prices

    return parts

def get_coolers(manufacturer,color,socket_compatibility,max_heatsink_height,min_heatsink_height,fan,radiator_size):
    part_query = {}
    if manufacturer is not None:
        part_query['Manufacturer'] = manufacturer
    if color is not None:
        part_query['color'] = color
    if socket_compatibility is not None:
        part_query['socket_compatilibity'] = socket_compatibility
    if min_heatsink_height is not None and max_heatsink_height:
        part_query['Maximum heatsink heigth'] = {'$in', [min_heatsink_height, max_heatsink_height]}
    elif min_heatsink_height is not None:
        part_query['Maximum heatsink heigth'] = {'$gt', min_heatsink_height}
    elif max_heatsink_height is not None:
        part_query['Maximum heatsink heigth'] = {'$lt', max_heatsink_height}
    if radiator_size is not None:
        part_query['radiator_size'] = radiator_size
    
    part_query['fan'] = fan

    pcpartpicker_response = requests.get(pcpartpicker_service_url+'/parts', params={'query_parameters':part_query})
    part_info_list = json.loads(pcpartpicker_response.json)
    
    sku_list = []
    for part_info in part_info_list:
        sku_list.append(part_info['Part #'])
    
    # Request prices from price-services
    chiptec_response = requests.get(chiptec_service_url+'/parts', params={'sku_list':sku_list})
    chiptec_prices = json.loads(chiptec_response.json)
    
    globaldata_response = requests.get(globaldata_service_url+'/parts', params={'sku_list':sku_list})
    globaldata_prices = json.loads(globaldata_response.json)
    
    clickfield_response = requests.get(clickfield_service_url+'/parts', params={'sku_list':sku_list})
    clickfield_prices = json.loads(clickfield_response.json)
    
    parts = []
    for part_info in part_info_list:
        part = {}
        part['sku'] = part_info['Part #']
        part['part_info'] = part_info
        prices = []
        prices.append({'chiptec':get_price_from_sku(chiptec_prices, part['sku'])})
        prices.append({'globaldata':get_price_from_sku(globaldata_prices, part['sku'])})
        prices.append({'clickfield':get_price_from_sku(clickfield_prices, part['sku'])})
        part['prices'] = prices

    return parts
    
    
def search_part(sku):
    pcpartpicker_response = requests.get(pcpartpicker_service_url+'/parts/'+sku)
    part_info = json.loads(pcpartpicker_response.json)
    
    chiptec_response = requests.get(chiptec_service_url+'/parts/'+sku)
    chiptec_price = json.loads(chiptec_response.json)
    
    globaldata_response = requests.get(globaldata_service_url+'/parts/'+sku)
    globaldata_price = json.loads(globaldata_response.json)
    
    clickfield_response = requests.get(clickfield_service_url+'/parts/'+sku)
    clickfield_price = json.loads(clickfield_response.json)
    
    part = []
    part.append(part_info)
    
    prices = []
    prices.append(chiptec_price)
    prices.append(globaldata_price)
    prices.append(clickfield_price)
    
    part.append(prices)
    
    