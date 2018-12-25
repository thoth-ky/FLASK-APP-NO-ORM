from unittest import TestCase
from ..app import create_flask_app
from ..app.models.models import DB, User


class BaseTestCase(TestCase):
  def setUp(self):
    self.app = create_flask_app(config_name='testing')

    self.client = self.app.test_client()
    self.user_table = User
    dsn = self.app.config.get("DATABASE_URL")
    self.db = DB(dsn)
    self.db.create_tables()
    self.user_info = {
      'username': 'user',
      'email': 'user@example.com',
      'password': 'password' 
    }

  def tearDown(self):
    self.db.destroy_tables()