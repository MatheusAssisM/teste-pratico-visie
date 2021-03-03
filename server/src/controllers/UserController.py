import http.server
from services.PessoaService import PessoaService
from jinja2 import FileSystemLoader, Environment
import json

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self._set_headers(200)

            if self.path == "/":
                data = self.getDataToJinja()
                self.getTemplate(data, "styles.html", "./templates")

            return 
        except:
            self._set_headers(400)
            return

    def do_POST(self):
        pararm = self.getUrlPararm(self.path)
        if self.path == "/":
            self._set_headers(201)

            postRequest = self.rfile.read(int(self.headers['Content-Length']))

            formData = self.cleanPostData(postRequest)
            self.createPessoa(formData)

        elif self.path[1::] == pararm:
            isExistsPessoa = self.findById(pararm)
            if isExistsPessoa:
                self._set_headers(204)
                self.deleteById(pararm)
                
                return
            else:
                self._set_headers(400)
                return
        else:
            self._set_headers(400)
            return

    def getUrlPararm(self, path):
        response = path[1::]
        return response

    def getDataToJinja(self):
        date, data = self.listAll()
        data = {
            "title": "Visie - Teste Prático",
            "data": data,
            "date": date,
            "counter":-1
            # "columns": self.getAllCollumnsNames()
        }
        return data

    def listAll(self):
        pessoa = PessoaService()            
        response = pessoa.getAll()
        formatedDate = []
        
        for i in range(len(response)):
            stringDate = str(response[i][5])
            stringDateList = stringDate.split("-")
            auxList = []
            for x in range(len(stringDateList)):
                lastItem = stringDateList[-1]
                auxList.append(lastItem)
                del stringDateList[-1]
                if x == len(stringDateList):
                    formatedDate.append(auxList)
        return formatedDate, response 

    def cleanPostData(self, post):
        data = post.decode()
        myDict = json.loads(data)        
        return myDict

    def getTemplate(self, data, file, dir):
        fileLoader = FileSystemLoader(dir)
        env = Environment(loader=fileLoader)
        template = env.get_template(file)
        output = template.render(data = data)
        return self.wfile.write(output.encode())

    def _set_headers(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def createPessoa(self, obj):
        pessoa = PessoaService()
        pessoa.create(obj)
        return

    def deleteById(self, id):
        pessoa = PessoaService()
        pessoa.deleteById(id)
        return
    
    def deleteAll(self):
        pessoa = PessoaService()
        pessoa.deleteAll()
        return 


    def getAllCollumnsNames(self):
        pessoa = PessoaService()            
        response = pessoa.getCollumnsNames()
        return response
    
    def findById(self, id):
        pessoa = PessoaService()
        response =  pessoa.findOne(id)
        return response
        