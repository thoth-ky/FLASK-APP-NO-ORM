from flask import Flask
from ..config import config_dict


def create_flask_app(config_name):
  app =Flask(__name__)
  app.config.from_object(config_dict[config_name])
  app.app_context().push()
  return app