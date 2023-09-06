import os
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_restful import Resource,Api

app = None
api=None
def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api=Api(app)
    app.app_context().push()
    return app,api

app, api = create_app()

# Import all the controllers so they are loaded
from application.controllers import *
from application.api import SendImage_Logs, UserAPI,TrackerAPI,LoggerAPI,SendImage_Logs
api.add_resource(UserAPI,"/api/<string:user_id>/<string:password>",'/api/user/create')
api.add_resource(TrackerAPI,"/api/<string:user_id>/<string:password>/<string:Tracker_Id>",'/api/<string:user_id>/<string:password>/CreateTracker')
api.add_resource(LoggerAPI,"/api/<string:user_id>/<string:password>/<string:Tracker_Id>/<string:Logger_Id>",'/api/<string:user_id>/<string:password>/<string:Tracker_Id>/CreateLogs')
api.add_resource(SendImage_Logs,"/api/<string:user_id>/<string:password>/<string:Tracker_Id>/Trendline&Stats")
if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080)
