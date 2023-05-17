from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import analysis_parent
import openai

#flask api initializer
app = Flask(__name__)
api = Api(app)
CORS(app)

#api class
class MoodAi(Resource):
    #entry point for endpoint
    def get(self, video_link, openaikey):
        
        data = {
            "image_results": [],
            "error": ""
        }

        try:
            openai.api_key = openaikey
            openai.Completion.create(
                engine='davinci',
                prompt='test openai key',
                max_tokens = 5
            )

            data["image_results"] = analysis_parent.main(video_link, openaikey)
        except (Exception, OSError, TypeError, openai.error.AuthenticationError)  as e:
            data["image_results"] = None
            data["error"] = str(e)

        return data
    
api.add_resource(MoodAi, '/moodai/<path:video_link>/<string:openaikey>')

if __name__ == '__main__':
    app.run(debug=False)