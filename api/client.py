from flask_restful import Resource
from flask import jsonify
from flask import request
from sqlalchemy import create_engine
from sqlalchemy import exc
import simplejson
import argon2
import os

db_connect = create_engine('sqlite:///data/db/clientbase.db')

class Client(Resource):

    def get(self):
        clientid = request.args.get('clientid')
        if clientid == None:
            conn = db_connect.connect() # connect to database
            query = conn.execute("select ID from clients") # performs query
            #cherrypy.log("{}: Pegou IDs de todos clientes".format(cherrypy.request.headers['Remote-Addr'])) # add on log
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
            #cherrypy.log("{}: Pegou dados de cliente(s) com ID = {}".format(cherrypy.request.headers['Remote-Addr'], clientid)) # add on log
            return jsonify(result)

    def post(self):
        #cherrypy.log("{}: Cadastrando usuario".format(cherrypy.request.headers['Remote-Addr'])) # add on log
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        cep = data.get("cep")
        phone1 = data.get("phone1")
        phone2 = data.get("phone2")
        cpf = data.get("cpf")
        password = data.get("password")
        birthday = data.get("birthday")
        sex = data.get("sex")

        # Encrypting the password
        salt = os.urandom(16)
        pas = argon2.argon2_hash(password, salt)
        pas = salt + pas
        
        try:
            conn = db_connect.connect()
            query = conn.execute("insert into clients (Name, Email, CEP, Phone1, Phone2, CPF, Password, Birthday, Sex)"
                                             " values (?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, email, cep, phone1, phone2, cpf, pas, birthday, sex))
            new_id = query.lastrowid
            #cherrypy.log("{}: Inseriu cliente com ID = {} e email = {}".format(cherrypy.request.headers['Remote-Addr'], new_id, email)) # add on log
            return {"Teste PUT":"Success", "Client ID":new_id}#jsonify(query.cursor) - esta dando erro
        except exc.IntegrityError:
            #cherrypy.log("{}: Tentou inserir cliente com email = {}. Email já cadastrado".format(cherrypy.request.headers['Remote-Addr'], email)) # add on log
            #cherrypy.response.status = 500
            return {'Code':1, 'Message':'Email already registered'}, 500
        return {"POST":"Success"}
            
    def put(self):
        #Update clients
        return {"PUT":"Success"}

    def delete(self):
        clientid = request.args.get('clientid')
        if clientid is None:
            return {"Code":1, "Message":"Parameter Missing"}, 500
        sql = "DELETE FROM clients WHERE ID=?"
        for i in range(1, len(clientid)):
            sql += " OR ID=?"
        sql += ";"
        conn = db_connect.connect()
        conn.execute(sql, clientid)
        #cherrypy.log("{}: Removeu cliente(s) com ID = {}".format(cherrypy.request.headers['Remote-Addr'], clientid)) # add on log
        return {"DELETE":"Success"}
        
        
        
        
        
