import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)
#utilizamos limit para que nos devuelva 10 medicamentos
r1 = conn.getresponse()
print(r1.status, r1.reason)
codigo_json = r1.read().decode("utf-8")
conn.close()

esquema_json = json.loads(codigo_json)
#recorremos cada elemento de la lista de los valores de la clave 'results'
for i in range(len (esquema_json['results'])):
    medicamento_info=esquema_json['results'][i]
    #imprimimos el id de cada medicamento
    print ('ID: ',medicamento_info['id'])

