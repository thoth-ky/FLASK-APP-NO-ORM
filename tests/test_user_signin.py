import json
from ..tests import BaseTestCase


class TestModelsSetUp(BaseTestCase):
  def test_user_signup(self):
    self.user_table().new(**self.user_info).save()
    response = self.client.post(
      '/auth/signin',
      data=json.dumps(self.user_info),
      content_type='application/json'
    )
    self.assertEqual(200, response.status_code)
    expected = "User successfully logged in."
    self.assertEqual(expected, json.loads(response.data)["message"])

  def test_duplicate_signin_with_wrong_credentials(self):
    self.user_table().new(**self.user_info).save()
    response = self.client.post(
      '/auth/signin',
      data=json.dumps(self.user_info_wrong_login),
      content_type='application/json'
    )
    self.assertEqual(401, response.status_code)
    expected = "Username or password is incorrect."
    self.assertEqual(expected, json.loads(response.data)["message"])
