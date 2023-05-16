from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse

#flask api initializer
app = Flask(__name__)
api = Api(app)

#api class
class MoodAi(Resource):

    def get(self, video_link, openaikey):
        return {"data": video_link}
        
    
api.add_resource(MoodAi, '/moodai/<string:video_link>/<string:openaikey>')

if __name__ == '__main__':
    app.run(debug=True)