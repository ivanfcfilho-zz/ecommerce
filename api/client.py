from flask_restful import Resource
from flask import jsonify
from flask import request
from sqlalchemy import create_engine
from sqlalchemy import exc
import logging
import argon2
import os

db_connect = create_engine('sqlite:///data/db/clientbase.db')

class Client(Resource):

    def get(self):
        clientid = request.args.get('clientid')
        if clientid == None:
            conn = db_connect.connect() # connect to database
            query = conn.execute("select ID from clients") # performs query
            logging.info("Pegou IDs de todos clientes") # add on log
            return {'clients': [i[0] for i in query.cursor.fetchall()]} #fetches the id from all users
        else:
            # Select all data, but password
            sql = "SELECT Name, Email, CEP, Phone1, Phone2, CPF, Birthday, Sex, Active FROM clients WHERE ID=?"
            for i in range(1, len(clientid)):
                sql += " OR id=?"
            sql += ";"
            conn = db_connect.connect()
            query = conn.execute(sql, clientid)
            result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
            logging.info("Pegou dados de cliente(s) com ID = {}".format(clientid)) # add on log
            return jsonify(result)

    def post(self):
        data = request.get_json()
        if data is None:
            return {'Code':2, 'Message':'Missing Parameter'}, 500
        email = data.get("email")
        name = data.get("name")
        cep = data.get("cep")
        phone1 = data.get("phone1")
        phone2 = data.get("phone2")
        cpf = data.get("cpf")
        password = data.get("password")
        birthday = data.get("birthday")
        sex = data.get("sex")
        if email is None or name is None or phone1 is None or cpf is None or password is None :
            return {'Code':2, 'Message':'Missing Parameter'}, 500

        # Encrypting the password
        salt = os.urandom(16)
        pas = argon2.argon2_hash(password, salt)
        pas = salt + pas
        
        try:
            conn = db_connect.connect()
            query = conn.execute("insert into clients (Name, Email, CEP, Phone1, Phone2, CPF, Password, Birthday, Sex)"
                                             " values (?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, email, cep, phone1, phone2, cpf, pas, birthday, sex))
            new_id = query.lastrowid
            logging.info("Inseriu cliente com ID = {} e email = {}".format(new_id, email)) # add on log
            return {"Message":"Post Success", "Client ID":new_id}
        except exc.IntegrityError:
            logging.info("Tentou inserir cliente com email = {}. Email já cadastrado".format(email)) # add on log
            return {'Code':1, 'Message':'Email already registered'}, 500
        return {'Code':3, 'Message':'Internal Error'}, 500
            
    def put(self):
        data = request.get_json()
        if data is None:
            return {'Code':2, 'Message':'Missing Parameter'}, 500
        dic = {}
        clientid = data.get("clientid")
        name = data.get("name")
        cep = data.get("cep")
        phone1 = data.get("phone1")
        phone2 = data.get("phone2")
        cpf = data.get("cpf")
        birthday = data.get("birthday")
        sex = data.get("sex")
        dic["name"] = name
        dic["cep"] = cep
        dic["phone1"] = phone1
        dic["phone2"] = phone2
        dic["cpf"] = cpf
        dic["birthday"] = birthday
        dic["sex"] = sex
        
        query = "UPDATE clients SET "
        for key, value in dic.items():
            if value is not None:
                query += key + " = '" + str(value) + "', "
        query = query[:-2] + " "
        query += "WHERE ID = " + clientid + ";" 
        
        try:
            conn = db_connect.connect()
            conn.execute(query)
            logging.info("Atualizou cliente com ID={}".format(clientid)) # add on log
            return {"Message":"Put Success"}
        except exc.IntegrityError:
            logging.info("Erro ao tentar fazer update:"+query) # add on log
            return {'Code':1, 'Message':'Internal Error'}, 500

    def delete(self):
        clientid = request.args.get('clientid')
        if clientid is None:
            return {"Code":1, "Message":"Parameter Missing"}, 500
        sql = "UPDATE clients SET Active = 'FALSE' WHERE ID=?"
        for i in range(1, len(clientid)):
            sql += " OR ID=?"
        sql += ";"
        conn = db_connect.connect()
        conn.execute(sql, clientid)
        logging.info("DEsativou cliente(s) com ID = {}".format(clientid)) # add on log
        return {"Message":"Delete Success"}
        
        
        
        
        
