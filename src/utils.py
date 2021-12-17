from flask import Response
import json

def returnJSON(code, message, reponse = {}):
   retJSON = {"code": code, "message": message, "response": reponse}
   resp = Response(json.dumps(retJSON, indent = 4), content_type='application/json; charset=utf-8', headers="")
   resp.headers['Access-Control-Allow-Origin'] = '*'
   return resp
