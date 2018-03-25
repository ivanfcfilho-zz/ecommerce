import cherrypy

@cherrypy.expose
class Client(object):
    @cherrypy.tools.accept(media='application/json')

    @cherrypy.tools.json_out()
    def GET(self, clients=None):
        #If clients is null return all, else execute a search query
        return {"Teste GET":"Success"}

    @cherrypy.tools.json_out()
    def POST(self, clients=None):
        #Register a client
        return {"Teste POST":"Success"}
     
    @cherrypy.tools.json_out()
    def PUT(self, clients=None):
        #Update clients
        return {"Teste PUT":"Success"}

    @cherrypy.tools.json_out()
    def DELETE(self, clients=None):
        #Remove clients
        return {"Teste DELETE":"Success"}
