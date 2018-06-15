from flask_restful import Resource
from flask import jsonify
from flask import request
import psycopg2
import logging
import os

connect_str = "dbname=d5th3ut0vlb2n5 user=hyohrpyibspjlg " \
              "host=ec2-54-83-19-244.compute-1.amazonaws.com " \
                  "password=9429157fb304bad69a62bdcb80c0a59de382830e03be8fa30450bdde368fd5f6 " \
                  "port=5432"

class Client(Resource):

    def get(self):
        clientid = request.args.get('clientid')
        email = request.args.get('email')
        if clientid:
            # Select all data, but password
            sql = "SELECT Name, Email, CEP, Phone1, Phone2, CPF, Birthday, Sex, Active FROM clients WHERE ID={}".format(clientid)
            sql += ";"
            conn = psycopg2.connect(connect_str)
            cursor = conn.cursor()
            cursor.execute(sql, clientid)
            rows = cursor.fetchall()
            column_names = [row[0] for row in cursor.description]
            result = {'data': [dict(zip(tuple(column_names), row)) for row in rows]}
            logging.info("Pegou dados de cliente(s) com ID = {}".format(clientid)) # add on log
            return jsonify(result)
        elif email:
            # Select all data, but password
            sql = "SELECT ID, Name, CEP, Phone1, Phone2, CPF, Birthday, Sex, Active FROM clients WHERE Email='{}'".format(email)
            sql += ";"
            conn = psycopg2.connect(connect_str)
            cursor = conn.cursor()
            cursor.execute(sql, clientid)
            rows = cursor.fetchall()
            column_names = [row[0] for row in cursor.description]
            result = {'data': [dict(zip(tuple(column_names), row)) for row in rows]}
            logging.info("Pegou dados de cliente(s) com Email = '{}'".format(email)) # add on log
            return jsonify(result)
        else:
            conn = psycopg2.connect(connect_str) # connect to database
            cursor = conn.cursor()
            cursor.execute("select ID from clients WHERE Active = 'TRUE'") # performs query
            logging.info("Pegou IDs de todos clientes") # add on log
            return {'clients': [i[0] for i in cursor.fetchall()]} #fetches the id from all users


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
            return {'Code':2, 'Message':'Faltando parametros'}, 500
        if phone2 is None: 
            phone2 = "null"
        if birthday is None: 
            birthday = "null"
        if sex is None: 
            sex = "true"

        try:
            conn = psycopg2.connect(connect_str)
            cursor = conn.cursor()
            logging.info("insert into clients (Name, Email, CEP, Phone1, Phone2, CPF, Password, Birthday, Sex)"
                                             " values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}') RETURNING id;".format(name, email, cep, phone1, phone2, cpf, password, birthday, sex))
            cursor.execute("insert into clients (Name, Email, CEP, Phone1, Phone2, CPF, Password, Birthday, Sex)"
                                             " values (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;", (name, email, cep, phone1, phone2, cpf, password, birthday, sex))
            new_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            logging.info("Inseriu cliente com ID = {} e email = {}".format(new_id, email)) # add on log
            #cursor.execute("select * from clients;")
            #rows = cursor.fetchall()
            return {"Message":"Post Success", "Client ID":new_id}
        except (Exception, psycopg2.DatabaseError) as error:
            logging.info(error)
            if error.pgcode == '23505':
                return {'Code': 1, 'Message': 'Email já existe.'}, 500
            return {'Code':3, 'Message':'Erro nos dados passados, verifique se está passando todos os dados necessários e se estão no formato correto.'}, 500

    def put(self):
        data = request.get_json()
        if data is None:
            return {'Code':2, 'Message':'Missing Parameter'}, 500
        dic = {}
        clientid = data.get("ID")
        email = data.get("email")
        if clientid:
            conn = psycopg2.connect(connect_str)
            cursor = conn.cursor()
            cursor.execute("select 1 from clients where ID = {};".format(clientid))
            rows = cursor.fetchone()
            logging.info(rows)  # add on log
            if rows is None:
                return {'Code': 1, 'Message': 'Client does not exist'}, 500
        elif email:
            conn = psycopg2.connect(connect_str)
            cursor = conn.cursor()
            cursor.execute("select 1 from clients where Email = '{}';".format(email))
            rows = cursor.fetchone()
            logging.info(rows)  # add on log
            if rows is None:
                return {'Code': 1, 'Message': 'Client does not exist'}, 500
        else:
            return {'Code':2, 'Message':'Missing Parameter: ID or Email.'}, 500

        dic["name"] = data.get("name")
        dic["cep"] = data.get("cep")
        dic["phone1"] = data.get("phone1")
        dic["phone2"] = data.get("phone2")
        dic["cpf"] = data.get("cpf")
        dic["birthday"] = data.get("birthday")
        dic["sex"] = data.get("sex")

        query = "UPDATE clients SET "
        for key, value in dic.items():
            if value is not None:
                query += key + " = '" + str(value) + "', "
        query = query[:-2] + " "
        if clientid is not None:
            query += "WHERE ID = " + str(clientid) + ";"
        else:
            query += "WHERE Email = '" + str(email) + "';"
        
        try:
            conn = psycopg2.connect(connect_str)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()

            logging.info("Atualizou cliente com ID={} ou Email={}".format(clientid, email)) # add on log
            return {"Message":"Put Success"}
        except:
            logging.info("Erro ao tentar fazer update:"+query) # add on log
            return {'Code':3, 'Message':'Internal Error'}, 500

    def delete(self):
        clientid = request.args.get('clientid')
        if clientid is None:
            return {"Code":1, "Message":"Parameter Missing"}, 500
        sql = "UPDATE clients SET Active = 'FALSE' WHERE ID={}".format(clientid[0])
        for i in range(1, len(clientid)):
            sql += " OR ID={}".format(clientid[i])
        sql += ";"
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        cursor.execute(sql, clientid)
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Desativou cliente(s) com ID = {}".format(clientid)) # add on log
        return {"Message":"Delete Success"}


class ClientEmail(Resource):

    def put(self):
        data = request.get_json()
        if data is None:
            return {'Code':1, 'Message': 'Missing Parameter'}, 500

        email = data.get("email")
        password = data.get("password")
        new_email = data.get("new_email")
        logging.info("Passou dados: email = "+email+", password = "+password+", new_email = "+new_email)
        if not(email and password and new_email):
            return {'Code':1, 'Message': 'Missing Parameters. Required: email, password, new_email'}, 500

        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        cursor.execute("select ID from clients where Email = %s and Password = %s;", (email, password))
        rows = cursor.fetchone()
        logging.info(rows)
        if rows is None:
            return {'Code':2, 'Message': 'Email or password does not match'}, 500

        query = "Atualizou cliente com ID=%s de Email=%s para novo Email=%s"
        try:
            conn = psycopg2.connect(connect_str)
            cursor = conn.cursor()
            cursor.execute("UPDATE clients SET Email=%s WHERE ID = %s", (new_email, rows))
            conn.commit()
            cursor.close()
            conn.close()
            logging.info("Atualizou cliente com ID=%s de Email=%s para novo Email=%s", (rows, email, new_email))  # add on log
            return {"Message": "Put Success"}
        except:
            logging.info("Erro ao tentar fazer mudança de email: " + query, (rows, email, new_email))  # add on log
            return {'Code': 3, 'Message': 'Internal Error'}, 500
