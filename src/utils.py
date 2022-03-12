from flask import Response
from json import dumps

def returnJSON(code, message, reponse = {}):
   retJSON = {"code": code, "message": message, "response": reponse}
   return Response(dumps(retJSON, indent = 4), content_type='application/json; charset=utf-8', headers="")
