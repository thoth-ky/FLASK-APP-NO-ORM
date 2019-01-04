from flask import Flask
from flask_restful import Api
from ..config import config_dict
from .views.user_signup import SignUp
from .views.user_signin import SignIn


def create_flask_app(config_name):
  app =Flask(__name__)
  app.config.from_object(config_dict[config_name])
  app.app_context().push()
  api = Api(app)
  api.add_resource(SignUp, '/auth/signup')
  api.add_resource(SignIn, '/auth/signin')
  return app