import cherrypy
from sqlalchemy import create_engine
import datetime
import argon2
import jwt

db_connect = create_engine('sqlite:///clientbase.db')
secret = 'qualquercoisa'

@cherrypy.expose
class UserAccess(object):
    @cherrypy.tools.accept(media='application/json')

    @cherrypy.tools.json_out()
    def GET(self, token=None):
        if token is None:
            return {'Code':1, 'Message':'Missing Input'}
        try:
            jwt.decode(token, secret, algorithm='HS256')
            return {"Teste GET":"Success"} # token valido
        except jwt.exceptions.ExpiredSignatureError:
            return {'Code':2, 'Message':'Token Expired'}
        except jwt.exceptions.InvalidTokenError:
            return {'Code':3, 'Message':'Invalid Token'}
    
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self, client=None):
        conn = db_connect.connect()
        input_json = cherrypy.request.json
        email = input_json["email"]
        password = input_json["password"]
        
        query = conn.execute("select Password from clients where Email=?", email)
        result = query.cursor.fetchone()[0]
        salt = result[:16]
        pas_true = result[16:]
        pas = argon2.argon2_hash(password, salt)
        if pas == pas_true:
            payload = {'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=1) } #token dura 1h
            token = jwt.encode(payload, secret, algorithm='HS256')
            json_out = {'token':token}
            return json_out
        return {"Code 3":"Password or email do not match"}
