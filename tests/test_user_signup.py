import json
from ..tests import BaseTestCase


class TestModelsSetUp(BaseTestCase):
  def test_user_signup(self):
    response = self.client.post(
      '/auth/signup',
      data=json.dumps(self.user_info),
      content_type='application/json'
    )
    self.assertEqual(201, response.status_code)
    expected = "User successfully registered. Proceed to log in."
    self.assertEqual(expected, json.loads(response.data)["message"])

  def test_duplicate_signup(self):
    self.user_table().new(**self.user_info).save()
    response = self.client.post(
      '/auth/signup',
      data=json.dumps(self.user_info),
      content_type='application/json'
    )
    self.assertEqual(400, response.status_code)
    expected = "Username has been taken. Kindly choose another"
    self.assertEqual(expected, json.loads(response.data)["message"])
