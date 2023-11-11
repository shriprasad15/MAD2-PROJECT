from flask_restful import Resource, Api
class Homepage(Resource):
    def get(self):
        return {"hello": "World"}

