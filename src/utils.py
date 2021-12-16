from flask import Response
import json

def returnJSON(code, message, reponse = {}):
   retJSON = {"code": code, "message": message, "response": reponse}
   return Response(json.dumps(retJSON, indent = 4), mimetype='application/json')
