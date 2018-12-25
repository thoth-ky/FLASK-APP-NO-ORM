from ..tests import BaseTestCase


class TestModelsSetUp(BaseTestCase):
  def create_user_in_db(self):
    return self.user_table().new(**self.user_info)
  
  def test_can_save_user_new(self):
    user = self.create_user_in_db()
    user.save()
    self.assertEqual(user.user_id, 1)
  
  def test_can_retrieve_record_by_id(self):
    user_created = self.create_user_in_db()
    user_created.save()
    self.assertEqual(user_created.user_id, 1)
    user_id = user_created.user_id
    retrieved = self.user_table().get_one_where('user_id', user_id)
    self.assertEqual(user_created.username, retrieved.username)
    # check if retrieved user asserts true the original password
    self.assertTrue(retrieved.check_password(self.user_info['password']))
    self.assertFalse(retrieved.check_password('wrongpassword'))
