import cherrypy
from api.client import Client
from api.user_access import UserAccess
import os

if __name__ == '__main__':
    rest_conf = {
        '/': {
            'tools.sessions.on': True,
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
            'log.access_file': 'log_access_file.txt',
            'log.error_file': 'log_application_file.txt'
        },
    }
    cherrypy.config.update({
        'tools.encode.on': True,
        'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.gzip.on': False,
        'environment': 'production',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    })

    cherrypy.tree.mount(Client(),           '/api/client/',     rest_conf)
    cherrypy.tree.mount(UserAccess(),       '/api/useraccess/',  rest_conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
