import cherrypy
from sqlalchemy import create_engine
from flask_jsonpify import jsonify
import simplejson
import argon2
import os

db_connect = create_engine('sqlite:///clientbase.db')

@cherrypy.expose
class Client(object):
    @cherrypy.tools.accept(media='application/json')

    @cherrypy.tools.json_out()
    def GET(self, clientid=None):
        if clientid == None:
            conn = db_connect.connect() # connect to database
            query = conn.execute("select * from clients") # performs query
            return {'clients': [i[0] for i in query.cursor.fetchall()]} #fetches the id from all users
        else:
            conn = db_connect.connect()
            query = conn.execute("select * from clients where Id =%d "  %int(clientid))
            result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
            return jsonify(result)

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        conn = db_connect.connect()
        input_json = cherrypy.request.json
        name = input_json["name"]
        email = input_json["email"]
        cep = input_json["cep"]
        phone1 = input_json["phone1"]
        cpf = input_json["cpf"]
        password = input_json["password"]
        birthday = input_json["birthday"]

        # Encrypting the password
        salt = os.urandom(16)
        pas = argon2.argon2_hash(password, salt)
        pas = salt + pas
        
        query = conn.execute("insert into clients (Name, Email, CEP, Phone1, CPF, Password, Birthday)"
                                             " values (?, ?, ?, ?, ?, ?, ?)", (name, email, cep, phone1, cpf, pas, birthday))
        return {"Teste PUT":"Success"}#jsonify(query.cursor) - esta dando erro

    @cherrypy.tools.json_out()
    def PUT(self, clients=None):
        #Update clients
        return {"Teste PUT":"Success"}

    @cherrypy.tools.json_out()
    def DELETE(self, clients=None):
        if clients is None:
            return {"Code":1, "Message":"Parameter Missing"}
        sql = "DELETE FROM clients WHERE id=?"
        for i in range(1, len(clients)):
            sql += " AND id=?"
        sql += ";"
        conn = db_connect.connect()
        conn.execute(sql, clients)
        return {"Teste DELETE":"Success"}
        
        
        
        
        
