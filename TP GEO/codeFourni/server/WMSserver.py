#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import tuile
import os
import shutil
import hashlib

PORT_NUMBER = 4242


class WMSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/wms"):
            # Ici on récupère les valeurs de paramètres GET
            params = urlparse.parse_qs(urlparse.urlparse(self.path).query)
            print(params)

            if 'request' not in params or 'layers' not in params \
            or 'height' not in params or 'width' not in params \
            or 'srs' not in params or 'bbox' not in params :
                self.send_error(400,'Paramètres manquants')
            elif params['request'][0] != "GetMap" :
                self.send_error(400,'Requête non conforme')
            elif params['srs'][0][5:] != "3857" :
                self.send_error(400,"SRS non valide. Seul le 3857 est accepté.")
            
            else :
                layers = params['layers'][0]
                bbox = [float(i) for i in params["bbox"][0].split(',')]
             
            #On prépare le cache en affectant à une requête une clé en fonction de sa bbox
            if layers == "roads" : 
                key = str(sum(bbox))
            elif layers == "batiments" :
                key = str(sum(bbox)/2)
            
            #On encrypte en SHA256 la clé, afin de pouvoir avoir un identifiant unique pour chaque tuile
            result = hashlib.sha256(key.encode())
            cached_tuile = result.hexdigest()
            
            #On vérifie si la tuile existe déjà dans le dossier cache
            if  os.path.exists('./cache/'+cached_tuile):
                self.send_png_image('./cache/'+cached_tuile)
                print("Cached")
            
            #Sinon, on la génère et on la sauvegarde
            else :
                print("Not Cached")
                min_lon = bbox[0]
                max_lon = bbox[2]
                min_lat = bbox[1]
                max_lat = bbox[3]
                height = int(params['height'][0])
                width = int(params['width'][0])
                    
                if layers == "roads" :     
                    tuile.routes(min_lon, max_lon, min_lat, max_lat,width, height,cached_tuile)
                    self.send_png_image(cached_tuile)
                    shutil.move(cached_tuile,'./cache')
            
                elif layers == "batiments" :
                    tuile.batiments(min_lon, max_lon, min_lat, max_lat,width, height,cached_tuile)
                    self.send_png_image(cached_tuile)
                    shutil.move(cached_tuile,'./cache')  
                      
            return

        

    def send_plain_text(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=UTF-8')
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))

    def send_png_image(self, filename):
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_html_file(self, filename):
        self.send_response(200)
        self.end_headers()
        self.serveFile(filename)


if __name__ == "__main__":
    try:
        # Ici on crée un serveur web HTTP, et on affecte le traitement
        # des requêtes à notre releaseHandler ci-dessus.
        server = HTTPServer(('', PORT_NUMBER), WMSHandler)
        print('Serveur démarré sur le port ', PORT_NUMBER)
        print('Ouvrez un navigateur et tapez dans la barre d\'url :'
              + ' http://localhost:%d/' % PORT_NUMBER)

        # Ici, on demande au serveur d'attendre jusqu'à la fin des temps...
        server.serve_forever()

    # ...sauf si l'utilisateur l'interrompt avec ^C par exemple
    except KeyboardInterrupt:
        print('^C reçu, je ferme le serveur. Merci.')
        server.socket.close()
