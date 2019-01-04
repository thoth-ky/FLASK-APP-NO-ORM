from flask_restful import Resource
from flask import request
from ..models.models import User


class SignIn(Resource):
  def post(self):
    user_data = request.get_json()
    username = user_data.get('username')
    password = user_data.get('password')

    user = User().get_one_where('username', username)
    if not user:
      return {
        "message": "Username or password is incorrect."
      }, 401
    
    if user.check_password(password=password):
      return {
        "message": "User successfully logged in."
      }, 200
    return {
        "message": "Username or password is incorrect."
      }, 401


    