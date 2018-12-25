import os
from dotenv import load_dotenv, find_dotenv
from .app import create_flask_app
from .app.models.models import DB, User


load_dotenv(find_dotenv())

CONFIG = os.environ.get('APP_SETTINGS')

APP = create_flask_app(CONFIG)
DSN = APP.config.get("DATABASE_URL")

db = DB(dsn=DSN)

@APP.cli.command()
def create_tables():
  try:
    db.create_tables()
    print('>>>Successfully created tables')
  except:
    print('>>>An error occured during create tables operation')

@APP.cli.command()
def drop_tables():
  try:
    db.destroy_table()
    print('>>>Successfully dropped tables')
  except:
    print('>>>An error occured during drop tables operation')

@APP.shell_context_processor
def make_shell_context():
  return {
    'db': db,
    'User': User
  }

if __name__ == '__main__':
    APP.run()
