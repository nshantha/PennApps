import cherrypy
import cherrypy_cors
import decimal
import json
import os
from microseil import *


class DecimalEncoder(json.JSONEncoder):
    """Helper class to allow for json serialization of Decimal"""

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


@cherrypy.expose
class SafeMapWebService(object):
    """Exposes table query api at http://<host>:<port>/info"""

    def parse_query(self, response):
        """Returns a constructed sqlalchemy query from json query"""
        # body needed here
        return query, session

    def query_response_to_json(self, fields, data):
        """Returns query response (a list of tuples) into a python dictionary
        based off of the fields provided

        Args:
            fields: ([String]) Ordered list of fields which data refers to
            data: ([Tuple]) Response from sql query
        """

        ret = []
        for entry in data:
            json_data = {}
            for i in range(len(entry)):
                json_data[fields[i]] = entry[i]
            ret.append(json_data)
        return ret

    @cherrypy_cors.tools.preflight(
        allowed_methods=["GET", "DELETE", "POST", "PUT"])
    def OPTIONS(self):
        pass

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return "hello"

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        input_json = cherrypy.request.json
        query, session = self.parse_query(input_json)
        response = query.all()
        session.close()

        # serialize response into proper JSON using DecimalEncoder
        json_response = json.loads(
            json.dumps(self.query_response_to_json(input_json["fields"],
                                                   response),
                       cls=DecimalEncoder))
        return json_response


def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            'tools.CORS.on': True,
            'cors.expose.on': True,
        },
    }
    cherrypy_cors.install()
    cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)

    net_conf = get_user_config()["cherrypy"]
    cherrypy.server.socket_host = net_conf["host"]
    cherrypy.server.socket_port = net_conf["port"]

    webapp = Harpoon()
    cherrypy.quickstart(webapp, '/', conf)
