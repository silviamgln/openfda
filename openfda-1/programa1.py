import http.client
import json
#Hola ña
#Cabeceras, con la petición GET indicamos que navegador somos
headers = {'User-Agent': 'http-client'}

#Creamos una variable con función del módulo http que establece una conexión entre el
#navegador y Openfda
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
#impirmimos la respuesta que nos da el server
print(r1.status, r1.reason)
codigo_json = r1.read().decode("utf-8")
#leemos el contenido y lo metemos en una variable
#cerramos la conexión con openfda
conn.close()

#el modulo json nos carga el archivo como diccionarios y listas
esquema_json = json.loads(codigo_json)
medicamento_info=esquema_json['results'][0]

print ('ID: ', medicamento_info['id'])
print ('Purpose: ',medicamento_info['purpose'][0])
print ('Manufacture: ',medicamento_info['openfda']['manufacturer_name'])
