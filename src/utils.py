from flask import Response
import json

def returnJSON(code, message, content):
   retJSON = {"code": code, "message": message, "content": content}
   return Response(json.dumps(retJSON, indent = 4), mimetype='application/json')
