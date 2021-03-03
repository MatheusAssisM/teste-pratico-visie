from repositories.PessoaRepository import PessoaRepository

class PessoaService():
    def __init__(self):
        self.repository = PessoaRepository()
        pass

    def findOne(self, id):
        response = self.repository.findOne(id)
        return response

    def create(self, obj):
        self.repository.save(obj)
        return

    def deleteById(self, id):
        self.repository.deleteById(id)
        return
    
    def deleteAll(self):
        self.repository.deleteAll()
        return
    
    def getAll(self):
        response = self.repository.listAll()
        return response

    def getCollumnsNames(self):
        response = self.repository.getCollumnNames('pessoas')
        return response
