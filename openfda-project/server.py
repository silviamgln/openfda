import http.server
import http.client
import json
import socketserver

#OPENFDA habilita una API, escucha en el puerto 80 y habla protocolo http, envía archivos json
#Nuestro server es server/client escucha en el 8000

PORT=8000


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET

    def main_page(self):
        html = """
            <html>
                <head>
                    <title>OpenFDA App</title>
                </head>
                <body>
                    <h1>OpenFDA Client </h1>
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Drug List">
                        </input>
                    </form>
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Drug Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Company List">
                        </input>
                    </form>
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Company Search">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Warnings List">
                        </input>
                    </form>
                </body>
            </html>
                """
        return html
    def dame_web (self, lista):
        list_html = """
                                <html>
                                    <head>
                                        <title>OpenFDA Cool App</title>
                                    </head>
                                    <body>
                                        <ul>
                            """
        for item in lista:
            list_html += "<li>" + item + "</li>"

        list_html += """
                                        </ul>
                                    </body>
                                </html>
                            """
        return list_html

    def generic_results(self, limit=10):
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json" + "?limit=" + str(limit))
        print("/drug/label.json" + "?limit=" + str(limit))
        r1 = conn.getresponse()
        data_raw = r1.read().decode("utf8")
        data = json.loads(data_raw)
        resultados = data['results']
        return resultados

    #se ejecuta cuando alguien se conecte al server y pida un GET
    def do_GET(self):
        # Dividir entre el endpoint y los parametros
        #divide el self.path en dos cachos (ej: /listCompanies '?' limit10
        recurso = self.path.split("?")
        #significa que despues de /listCompanies te han pasado otro parámetro
        if len(recurso) > 1:
            params = recurso[1]
        else:
            params = ""

        #es 1 por defecto
        limit = 1

        # Obtener los parametros
        if params:
            print("Hay parametros")
            #limit=10 se queda limit[0] y 10[1]
            def_limit = params.split("=")
            #está limitada la respuesta
            if def_limit[0] == "limit":
                #limit = 10 ya que es la posición 1
                limit = int(def_limit[1])
                print("Limit: {}".format(limit))
        else:
            print("SIN PARAMETROS")




        # Write content as utf-8 data
        if self.path=='/':
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            #ese método construye la web de los formularios como un string
            html=self.main_page()
            self.wfile.write(bytes(html, "utf8"))

        #usamos in self.path ya que puedes ser /listDrugs?search etc, entonces pides
        #"si la palabra está en self.path" tal tal
        elif 'listDrugs' in self.path:
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            medicamentos = []
            resultados = self.generic_results(limit)
            for resultado in resultados:
                if ('generic_name' in resultado['openfda']):
                    medicamentos.append(resultado['openfda']['generic_name'][0])
                else:
                    medicamentos.append('Desconocido')
            resultado_html = self.dame_web (medicamentos)

            self.wfile.write(bytes(resultado_html, "utf8"))

        elif 'listCompanies' in self.path:
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            companies = []
            resultados = self.generic_results(limit)
            for resultado in resultados:
                if ('manufacturer_name' in resultado['openfda']):
                    companies.append(resultado['openfda']['manufacturer_name'][0])
                else:
                    companies.append('Desconocido')

            resultado_html = self.dame_web(companies)

            self.wfile.write(bytes(resultado_html, "utf8"))

        elif 'listWarnings' in self.path:
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            warnings = []
            resultados = self.generic_results(limit)
            for resultado in resultados:
                if ('warnings' in resultado):
                    warnings.append(resultado['warnings'][0])
                else:
                    warnings.append('Desconocido')
            resultado_html = self.dame_web(warnings)

            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'searchDrug' in self.path:
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Por defecto 10 en este caso, no 1
            limit = 10
            drug = self.path.split('=')[1]
            drugs = []
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json" + "?limit=" + str(limit) + '&search=active_ingredient:' + drug)
            r1 = conn.getresponse()
            data1 = r1.read()
            data = data1.decode("utf8")
            biblioteca_data = json.loads(data)
            events_search_drug = biblioteca_data['results']
            for resultado in events_search_drug:
                if ('generic_name' in resultado['openfda']):
                    drugs.append(resultado['openfda']['generic_name'][0])
                else:
                    drugs.append('Desconocido')

            resultado_html = self.dame_web(drugs)
            self.wfile.write(bytes(resultado_html, "utf8"))
        elif 'searchCompany' in self.path:
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Por defecto 10 en este caso, no 1
            limit = 10
            company = self.path.split('=')[1]
            companies = []
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json" + "?limit=" + str(limit) + '&search=openfda.manufacturer_name:' + company)
            r1 = conn.getresponse()
            data1 = r1.read()
            data = data1.decode("utf8")
            biblioteca_data = json.loads(data)
            events_search_company = biblioteca_data['results']

            for event in events_search_company:
                companies.append(event['openfda']['manufacturer_name'][0])
            resultado_html = self.dame_web(companies)
            self.wfile.write(bytes(resultado_html, "utf8"))

        #302 se utiliza para que devuelva una pag y una localización a la nueva pag web
        elif 'redirect' in self.path:
            self.send_error(302)
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()
        elif 'secret' in self.path:
            self.send_error(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()
        else:
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(self.path).encode())
        return



#Permite que se pueda reutilizar sin esperar el puerto 8000
socketserver.TCPServer.allow_reuse_address= True
#instancia de una clase que atiende a las peticiones http que pueden venir de un
#navegador o del test de prueba de la práctica
Handler = testHTTPRequestHandler
#Asocia una IP y puerto al manejador de peticiones
#llega la petición y se manda al manejador
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
#arranca el servidor
httpd.serve_forever()