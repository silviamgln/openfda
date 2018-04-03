import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", '/drug/label.json?limit=100&search=substance_name:"ASPIRIN"', None, headers)
#la petición va cambiando porque cambia el num de cosas que quieres pedir
#Dame 100 relacionados con la aspirina y sáltate los 0 primeros (el skip)
r1 = conn.getresponse()
print(r1.status, r1.reason)
codigo_json = r1.read().decode("utf-8")
conn.close()

esquema_json = json.loads(codigo_json)

for i in range (len (esquema_json['results'])):
    medicine_info=esquema_json['results'][i]
    print ('ID: ',medicine_info['id'])
    #recorremos todos los medicamentos imprimiendo el id

    if (medicine_info['openfda']):
        print('Manufacturer: ', medicine_info['openfda']['manufacturer_name'][0])

