from flask_restful import Resource
from sqlalchemy import create_engine
from flask import jsonify
from flask import request
import datetime
import argon2
import jwt

db_connect = create_engine('sqlite:///data/db/clientbase.db')
secret = 'qualquercoisa'

class UserAccess(Resource):

    def get(self):
        #cherrypy.log("{}: Tentando acessar area com autorização".format(cherrypy.request.headers['Remote-Addr'])) # add on log
        token = request.args.get('token')
        if token is None:
            #cherrypy.log("{}: Sem token".format(cherrypy.request.headers['Remote-Addr'])) # add on log
            return {'Code':1, 'Message':'Missing Input'}, 500
        try:
            jwt.decode(token, secret, algorithm='HS256')
            #cherrypy.log("{}: Token válido".format(cherrypy.request.headers['Remote-Addr'])) # add on log
            return # token valido
        except jwt.exceptions.ExpiredSignatureError:
            #cherrypy.log("{}: Token expirado".format(cherrypy.request.headers['Remote-Addr'])) # add on log
            return {'Code':2, 'Message':'Token Expired'}, 500
        except jwt.exceptions.InvalidTokenError:
            #cherrypy.log("{}: Token invalido".format(cherrypy.request.headers['Remote-Addr'])) # add on log
            return {'Code':3, 'Message':'Invalid Token'}, 500
    
    def post(self):
        #cherrypy.log("{}: Fazendo login".format(cherrypy.request.headers['Remote-Addr'])) # add on log
        # Get json input
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        # Get the password in the db
        conn = db_connect.connect()
        query = conn.execute("select Password from clients where Email=?", email)
        result = query.cursor.fetchone()
        if result is None:
            #cherrypy.log("{}: Email não encontrado".format(cherrypy.request.headers['Remote-Addr'])) # add on log
            {'Code':1, 'Message':"Password or email do not match"}, 500
        result = result[0]
        salt = result[:16]
        pas_true = result[16:]
        pas = argon2.argon2_hash(password, salt)
        
        # Compare the password
        if pas == pas_true:
            payload = {'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=1) } #token dura 1h
            token = jwt.encode(payload, secret, algorithm='HS256')
            json_out = {'token':token}
            #cherrypy.log("{}: Login com sucesso".format(cherrypy.request.headers['Remote-Addr'])) # add on log
            return jsonify(json_out)
        #cherrypy.log("{}: Senha errada".format(cherrypy.request.headers['Remote-Addr'])) # add on log
        return {'Code':1, 'Message':"Password or email do not match"}, 500
