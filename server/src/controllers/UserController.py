import http.server
from services.PessoaService import PessoaService
from jinja2 import FileSystemLoader, Environment
import json

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle to HTTP GET
        """
        try:
            self._set_headers(200)

            if self.path == "/":
                data = self.getDataToJinja()
                self.getTemplate(data, "styles.html", "./templates")

            return 
        except:
            self._set_headers(500)
            return

    def do_POST(self):
        """Handle two routes from POST
        """
        try:
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
        except:
            self._set_headers(500)
            return

    def getUrlPararm(self, path):
        """get pararm from URL

        Args:
            path (str): route from request

        Returns:
            str: the pararm
        """
        response = path[1::]
        return response

    def getDataToJinja(self):
        """get all data that will be send to Jinja template

        Returns:
            object: all data
        """
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
        """list all row on table

        Returns:
            list: list with all rows
        """
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
        """receive and clean post data

        Args:
            post (bytes): data from request

        Returns:
            dict: formated data
        """
        data = post.decode()
        myDict = json.loads(data)        
        return myDict

    def getTemplate(self, data, file, dir):
        """render the jinja template

        Args:
            data (dict): dict with all variables
            file (str): path
            dir (str): dir

        Returns:
            any: return rendered template
        """
        fileLoader = FileSystemLoader(dir)
        env = Environment(loader=fileLoader)
        template = env.get_template(file)
        output = template.render(data = data)
        return self.wfile.write(output.encode())

    def _set_headers(self, code):
        """Set headers to response

        Args:
            code (int): a HTTP code
        """
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def createPessoa(self, obj):
        """send the pessoa obj to be saved on DB

        Args:
            obj (object): pessoa object
        """
        pessoa = PessoaService()
        pessoa.create(obj)
        return

    def deleteById(self, id):
        """delete a pessoa by id

        Args:
            id (string): prymary key of pessoa
        """
        pessoa = PessoaService()
        pessoa.deleteById(id)
        return
    
    def deleteAll(self):
        """Delete all data from table
        """
        pessoa = PessoaService()
        pessoa.deleteAll()
        return 


    def getAllCollumnsNames(self):
        """get columns names and types

        Returns:
            list: response from DB
        """
        pessoa = PessoaService()            
        response = pessoa.getCollumnsNames()
        return response
    
    def findById(self, id):
        """find a row by id

        Args:
            id (str): row id

        Returns:
            list: list with all informations about the row
        """
        pessoa = PessoaService()
        response =  pessoa.findOne(id)
        return response
        