import requests

def test(sku):
    response = requests.get('chiptec_service.svc.cluster.local/part/'+sku)
    return response.json