from flask import Flask
from flask_restful import Api
from  api.client import Client
from api.user_access import UserAccess
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

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hyohrpyibspjlg:9429157fb304bad69a62bdcb80c0a59de382830e03be8fa30450bdde368fd5f6@ec2-54-83-19-244.compute-1.amazonaws.com:5432/d5th3ut0vlb2n5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api.add_resource(Client, '/api/client')
api.add_resource(UserAccess, '/api/useraccess')

if __name__ == '__main__':
    app.run(debug=True)
