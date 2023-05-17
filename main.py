from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
import analysis_parent

#flask api initializer
app = Flask(__name__)
api = Api(app)
CORS(app)

#api class
class MoodAi(Resource):
    #entry point for endpoint
    def get(self, video_link, openaikey):

        image_results = analysis_parent.main(video_link, openaikey)

        return image_results
    
api.add_resource(MoodAi, '/moodai/<path:video_link>/<string:openaikey>')

if __name__ == '__main__':
    app.run(debug=False)