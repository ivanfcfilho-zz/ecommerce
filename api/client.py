import cherrypy
from sqlalchemy import create_engine
from sqlalchemy import exc
import simplejson
import os

db_connect = create_engine('sqlite:///clientbase.db')

@cherrypy.expose
class Client(object):
    @cherrypy.tools.accept(media='application/json')

    @cherrypy.tools.json_out()
    def GET(self, clientid=None):
        if clientid == None:
            conn = db_connect.connect() # connect to database
            query = conn.execute("select ID from clients") # performs query
            cherrypy.log("{}: Pegou IDs de todos clientes".format(cherrypy.request.headers['Remote-Addr'])) # add on log
            return {'clients': [i[0] for i in query.cursor.fetchall()]} #fetches the id from all users
        else:
            # Select all data, but password
            sql = "SELECT Name, Email, CEP, Phone1, Phone2, CPF, Birthday, Sex FROM clients WHERE ID=?"
            for i in range(1, len(clientid)):
                sql += " OR id=?"
            sql += ";"
            conn = db_connect.connect()
            query = conn.execute(sql, clientid)
            result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
            cherrypy.log("{}: Pegou dados de cliente(s) com ID = {}".format(cherrypy.request.headers['Remote-Addr'], clientid)) # add on log
            return result

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        cherrypy.log("{}: Cadastrando usuario".format(cherrypy.request.headers['Remote-Addr'])) # add on log
        
        conn = db_connect.connect()
        input_json = cherrypy.request.json
        name = input_json["name"]
        email = input_json["email"]
        cep = input_json["cep"]
        phone1 = input_json["phone1"]
        phone2 = input_json["phone2"]
        cpf = input_json["cpf"]
        password = input_json["password"]
        birthday = input_json["birthday"]
        sex = input_json["sex"]

        # Encrypting the password
        #salt = os.urandom(16)
        #pas = argon2.argon2_hash(password, salt)
        #pas = salt + pas
        
        try:
            query = conn.execute("insert into clients (Name, Email, CEP, Phone1, Phone2, CPF, Password, Birthday, Sex)"
                                             " values (?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, email, cep, phone1, phone2, cpf, password, birthday, sex))
            new_id = query.lastrowid
            cherrypy.log("{}: Inseriu cliente com ID = {} e email = {}".format(cherrypy.request.headers['Remote-Addr'], new_id, email)) # add on log
            return {"Teste PUT":"Success", "Client ID":new_id}#jsonify(query.cursor) - esta dando erro
        except exc.IntegrityError:
            cherrypy.log("{}: Tentou inserir cliente com email = {}. Email já cadastrado".format(cherrypy.request.headers['Remote-Addr'], email)) # add on log
            cherrypy.response.status = 500
            return {'Code':1, 'Message':'Email already registered'}
            

    @cherrypy.tools.json_out()
    def PUT(self, clientid=None):
        #Update clients
        return {"Teste PUT":"Success"}

    @cherrypy.tools.json_out()
    def DELETE(self, clientid=None):
        if clientid is None:
            return {"Code":1, "Message":"Parameter Missing"}
        sql = "DELETE FROM clients WHERE ID=?"
        for i in range(1, len(clientid)):
            sql += " OR ID=?"
        sql += ";"
        conn = db_connect.connect()
        conn.execute(sql, clientid)
        cherrypy.log("{}: Removeu cliente(s) com ID = {}".format(cherrypy.request.headers['Remote-Addr'], clientid)) # add on log
        return {"Teste DELETE":"Success"}
        
        
        
        
        
