import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
codigo_json = r1.read().decode("utf-8")
conn.close()

#escribimos a fichero lo recibido
#fichero = open ('label.json', 'w')
#fichero.write(codigo_json)
#fichero.close()
#fin escribir


esquema_json = json.loads(codigo_json)
for i in range (len (esquema_json['results'])):
    medicamento_info=esquema_json['results'][i]

    print ('ID: ',medicamento_info['id'])
