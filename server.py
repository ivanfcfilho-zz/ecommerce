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
        },
    }

    cherrypy.tree.mount(Client(),           '/api/client/',     rest_conf)
    cherrypy.tree.mount(UserAccess(),       '/api/useraccess/',  rest_conf)

    cherrypy.engine.start()
    cherrypy.engine.block()
