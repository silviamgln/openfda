import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)
#Limit indica que el API nos tiene que devolver 10 medicamentos
#?limit=10&color=blue"
r1 = conn.getresponse()
print(r1.status, r1.reason)
codigo_json = r1.read().decode("utf-8")
conn.close()

esquema_json = json.loads(codigo_json)
for i in range (len (esquema_json['results']))
    #longitud de la lista de resultados
    medicine_info=esquema_json['results'][i]
    #cada resultado es un diccionario

    print ('ID: ',medicine_info['id'])
#cada resultado es un diccionario