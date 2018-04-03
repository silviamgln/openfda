import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
codigo_json = r1.read().decode("utf-8")
conn.close()

esquema_json = json.loads(codigo_json)
#el modulo json nos carga el archivo "en crudo" modo diccionarios y listas (estructura tipo python)
medicamento_info=esquema_json['results'][0]
#variable dentro de la carpeta results del json

print ('ID: ', medicamento_info['id'])
#buscamos la etiqueta 'id'
print ('Purpose: ',medicamento_info['purpose'][0])
print ('Manufacture: ',medicamento_info['openfda']['manufacturer_name'])
