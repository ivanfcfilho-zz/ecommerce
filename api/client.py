import cherrypy
from sqlalchemy import create_engine
from flask_jsonpify import jsonify
import simplejson

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
            query = conn.execute("select * from cients where EmployeeId =%d "  %int(clientid))
            result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
            return jsonify(result)

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def POST(self):
        conn = db_connect.connect()
        input_json = cherrypy.request.json
        id = 1                              #como fazer? random?
        name = input_json["name"]
        email = input_json["email"]
        cep = input_json["cep"]
        phone1 = input_json["phone1"]
        cpf = input_json["cpf"]
        sex = input_json["sex"]
        password = input_json["password"]
        birthday = input_json["birthday"]

        query = conn.execute("insert into clients (ID, Name, Email, CEP, Phone1, CPF, Password, Birthday)"
                                             " values ({}, '{}', '{}', '{}', '{}', '{}', '{}' '{}', '{}')"
                                             .format(id, name, email, cep, phone1, cpf, sex, password, birthday))
        return jsonify(query.cursor)

    @cherrypy.tools.json_out()
    def PUT(self, clients=None):
        #Update clients
        return {"Teste PUT":"Success"}

    @cherrypy.tools.json_out()
    def DELETE(self, clients=None):
        #Remove clients
        return {"Teste DELETE":"Success"}
