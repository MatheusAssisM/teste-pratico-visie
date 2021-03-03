from databases.config import (myDriver, myDB)
from datetime import datetime

class PessoaRepository():
    def __init__(self):
        self.driver = myDriver
        self.db = myDB
        pass
    
    def generateID(self):
        sql = """
        SELECT * FROM pessoas 
        WHERE id_pessoa=(SELECT max(id_pessoa) FROM pessoas);
        """
        self.driver.execute(sql)
        try:
            response = self.driver.fetchall()
            lastId = response[0][0]
            newId = str(lastId + 1)
            return newId
        except:
            return "1"

    def generateDataAdmissao(self):
        now = datetime.now()
        dateTime = now.strftime("%Y-%m-%d")
        return dateTime

    def findOne(self, id):
        sql = f"""
        SELECT * FROM pessoas
        WHERE id_pessoa = '{id}' 
        """
        self.driver.execute(sql)
        response = self.driver.fetchall()
        return response

    def listAll(self):
        sql = "SELECT * FROM pessoas"
        self.driver.execute(sql)
        response = self.driver.fetchall()
        return response
    
    def getCollumnNames(self, table):
        sql = f"""
        SELECT COLUMN_NAME, DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME ='{table}' 
        ORDER BY ORDINAL_POSITION
        """
        self.driver.execute(sql)
        response = self.driver.fetchall()
        return response

    def deleteById(self, id):
        sql = f"DELETE FROM pessoas WHERE id_pessoa = '{id}'"
        self.driver.execute(sql)
        self.db.commit()

    def deleteAll(self):
        sql = f"DELETE FROM pessoas"
        self.driver.execute(sql)
        self.db.commit()

    def save(self, obj):
        sql = f"""
        INSERT INTO pessoas (
            nome,
            rg,
            cpf,
            data_nascimento,
            funcao,
            id_pessoa,
            data_admissao
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        val = (
            obj["nome"], 
            obj["rg"], 
            obj["cpf"], 
            obj["data_nascimento"], 
            obj["funcao"],
            self.generateID(),
            self.generateDataAdmissao()
            )

        self.driver.execute(sql, val)
        self.db.commit()
        return 
        

        
