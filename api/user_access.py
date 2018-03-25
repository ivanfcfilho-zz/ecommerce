import cherrypy

@cherrypy.expose
class UserAccess(object):
    @cherrypy.tools.accept(media='application/json')

    @cherrypy.tools.json_out()
    def GET(self, token=None):
        #Check token ?
        return {"Teste GET":"Success"}
    
    @cherrypy.tools.json_out()
    def POST(self, client=None):
        #login
        return {"Test POST":"Success"}
