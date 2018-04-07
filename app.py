import cherrypy
from api.client import Client
from api.user_access import UserAccess

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

    cherrypy.tree.mount(Client(),           '/api/client/',     rest_conf)
    cherrypy.tree.mount(UserAccess(),       '/api/useraccess/',  rest_conf)
    cherrypy.config.update({'server.socket_port': 80})
    cherrypy.engine.start()
    cherrypy.engine.block()
