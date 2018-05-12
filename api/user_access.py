from flask_restful import Resource
import psycopg2
from flask import jsonify
from flask import request
import logging
import datetime
import argon2
import jwt

connect_str = "dbname=d5th3ut0vlb2n5 user=hyohrpyibspjlg " \
              "host=ec2-54-83-19-244.compute-1.amazonaws.com " \
                  "password=9429157fb304bad69a62bdcb80c0a59de382830e03be8fa30450bdde368fd5f6 " \
                  "port=5432"

secret = 'qualquercoisa'

class UserAccess(Resource):

    def get(self):
        logging.info("Tentando acessar area com autorizacao") # add on log
        token = request.args.get('token')
        if token is None:
            logging.info("{}: Sem token") # add on log
            return {'Code':1, 'Message':'Missing Input'}, 500
        try:
            token = token.encode()
            jwt.decode(token, secret, algorithm='HS256')
            logging.info("Token valido") # add on log
            return {"Message":"Success"}
        except jwt.exceptions.ExpiredSignatureError:
            logging.info("Token expirado") # add on log
            return {'Code':2, 'Message':'Token Expired'}, 500
        except jwt.exceptions.InvalidTokenError:
            logging.info("Token invalido") # add on log
            return {'Code':3, 'Message':'Invalid Token'}, 500
    
    def post(self):
        # Get json input
        data = request.get_json()
        if data is None:
            return {'Code':2, 'Message':'Missing Parameter'}, 500
        email = data.get("email")
        password = data.get("password")
        if email is None or password is None:
            return {'Code':2, 'Message':'Missing Parameter'}, 500
        
        logging.info("Fazendo login com email = {}".format(email)) # add on log
        # Get the password in the db
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        cursor.execute("select Password from clients where Email='{}'".format(email))
        result = cursor.fetchone()
        if result is None:
            logging.info("Email nao encontrado") # add on log
            return {'Code':1, 'Message':"Password or email do not match"}, 500
        #result = result[0]
        #salt = result[:16]
        logging.info("{}").format(result) # add on log
        pas_true = str(result)[2:]
        pas_true = pas_true[:-3]
        #pas = argon2.argon2_hash(password, salt)
        
        # Compare the password
        if password == pas_true:
            payload = {'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=1) } #token dura 1h
            token = jwt.encode(payload, secret, algorithm='HS256')
            token = token.decode("utf-8") 
            json_out = {'token':token}
            logging.info("Login com sucesso") # add on log
            return jsonify(json_out)
        logging.info("Senha errada") # add on log
        return {'Code':1, 'Message':"Password or email do not match"}, 500
