from flask import Flask
from flask_restful import Api
from client import Client
from user_access import UserAccess
from logging.config import dictConfig
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.FileHandler',
        'filename': 'log/log_file',
        'formatter': 'default'
    }, 'wsgi': {
        'class': 'logging.StreamHandler',
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'file']
    }
})


app = Flask(__name__)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/clientbase2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api.add_resource(Client, '/api/client')
api.add_resource(UserAccess, '/api/useraccess')

if __name__ == '__main__':
    app.run(debug=True)
