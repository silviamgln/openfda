import http.client
import json

headers = {'User-Agent': 'http-client'}

skip_num=0
while True:
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", '/drug/label.json?limit=100&skip='+str(skip_num)+'&search=substance_name:"ASPIRIN"', None, headers)
    #Nos devuelve 100 mediacamentosrelacionados con la aspirina
    #y salta los 0 primeros (el skip)
    #Al volverlo a ejecutar salta los 100 primeros
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    codigo_json = r1.read().decode("utf-8")
    conn.close()

    esquema_json = json.loads(codigo_json)

    for i in range (len (esquema_json['results'])):
        medicine_info=esquema_json['results'][i]
        #recorremos todos los medicamentos imprimiendo el id
        print ('ID: ',medicine_info['id'])

        #si el medicamento tiene manufacturer lo imprimimos también
        if (medicine_info['openfda']):
            print('Manufacturer: ', medicine_info['openfda']['manufacturer_name'][0])

    #Si se cumple esta condición el bucle while se para
    if (len(esquema_json['results'])<100):
        break
    skip_num=skip_num+100

