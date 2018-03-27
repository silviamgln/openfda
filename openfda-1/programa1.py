import http.client
import json

headers = {'User-Agent': 'http-client'}

#Cabeceras, con la petición GET indicamos que navegador somos

conn = http.client.HTTPSConnection("api.fda.gov")
#creamos una conexión con openfda al url de la api
conn.request("GET", "/drug/label.json", None, headers)
#pedimos el recurso
r1 = conn.getresponse()
#la respuesta que te da openfda
print(r1.status, r1.reason)
codigo_json = r1.read().decode("utf-8")
conn.close()

#escribimos a fichero lo recibido
#fichero = open ('label.json', 'w')
#fichero.write(label_raw)
#fichero.close()
#fin escribir


esquema_json = json.loads(codigo_json)
#la libreria json nos carga el archivo "en crudo"
medicamento_info=esquema_json['results'][0]


print ('ID: ', medicamento_info['id'])
print ('Purpose: ',medicamento_info['purpose'][0])

print ('Manufacture: ',medicamento_info['openfda']['manufacturer_name'][0])