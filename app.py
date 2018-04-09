from flask import Flask
from flask_restful import Api
from api.client import Client
from api.user_access import UserAccess
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/db/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api.add_resource(Client, '/api/client')
api.add_resource(UserAccess, '/api/useraccess')

if __name__ == '__main__':
    app.run(debug=True)
