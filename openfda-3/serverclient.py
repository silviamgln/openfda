import http.server
import socketserver
import http.client
import json

#Puerto donde lanzamos el servidor
PORT = 8004

def dame_lista():
    lista = []
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=10", None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    codigo_json = r1.read().decode("utf-8")
    conn.close()

    esquema_json = json.loads(codigo_json)
    for i in range(len(esquema_json['results'])):
        medicamento_info = esquema_json['results'][i]
        if (medicamento_info['openfda']):
            print('Fabricante: ', medicamento_info['openfda']['generic_name'][0])
            lista.append(medicamento_info['openfda']['generic_name'][0])

    return lista

# Creamos una clase que deriva de BaseHTTPRequestHandler
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)

        # En las cabeceras indicamos el contenido que le enviamos
        #al cliente, que será html
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content="<html><body>"
        lista=dame_lista ()
        for e in lista:
            content += e+"<br>"
        content+="</body></html>"
        self.wfile.write(bytes(content, "utf8"))
        return

# establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("El usuario ha interrumpido el servicio")
    pass

httpd.server_close()
print("")
print("Servicio parado")

