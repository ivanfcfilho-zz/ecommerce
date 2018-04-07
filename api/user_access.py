import cherrypy
from sqlalchemy import create_engine
import datetime
import argon2
import jwt

db_connect = create_engine('sqlite:///data/db/clientbase.db')
secret = 'qualquercoisa'

@cherrypy.expose
class UserAccess(object):
    @cherrypy.tools.accept(media='application/json')

    @cherrypy.tools.json_out()
    def GET(self, token=None):
        cherrypy.log("{}: Tentando acessar area com autorização".format(cherrypy.request.headers['Remote-Addr'])) # add on log
        if token is None:
            cherrypy.log("{}: Sem token".format(cherrypy.request.headers['Remote-Addr'])) # add on log
            return {'Code':1, 'Message':'Missing Input'}
        try:
            jwt.decode(token, secret, algorithm='HS256')
            cherrypy.log("{}: Token válido".format(cherrypy.request.headers['Remote-Addr'])) # add on log
            return {"Teste GET":"Success"} # token valido
        except jwt.exceptions.ExpiredSignatureError:
            cherrypy.log("{}: Token expirado".format(cherrypy.request.headers['Remote-Addr'])) # add on log
            return {'Code':2, 'Message':'Token Expired'}
        except jwt.exceptions.InvalidTokenError:
            cherrypy.log("{}: Token invalido".format(cherrypy.request.headers['Remote-Addr'])) # add on log
            return {'Code':3, 'Message':'Invalid Token'}
    
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self, client=None):
        cherrypy.log("{}: Fazendo login".format(cherrypy.request.headers['Remote-Addr'])) # add on log
        conn = db_connect.connect()
        input_json = cherrypy.request.json
        email = input_json["email"]
        password = input_json["password"]
        
        query = conn.execute("select Password from clients where Email=?", email)
        result = query.cursor.fetchone()
        if result is None:
            cherrypy.log("{}: Email não encontrado".format(cherrypy.request.headers['Remote-Addr'])) # add on log
            {'Code':1, 'Message':"Password or email do not match"}
        result = result[0]
        salt = result[:16]
        pas_true = result[16:]
        pas = argon2.argon2_hash(password, salt)
        if pas == pas_true:
            payload = {'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=1) } #token dura 1h
            token = jwt.encode(payload, secret, algorithm='HS256')
            json_out = {'token':token}
            cherrypy.log("{}: Login com sucesso".format(cherrypy.request.headers['Remote-Addr'])) # add on log
            return json_out
        cherrypy.log("{}: Senha errada".format(cherrypy.request.headers['Remote-Addr'])) # add on log
        return {'Code':1, 'Message':"Password or email do not match"}
