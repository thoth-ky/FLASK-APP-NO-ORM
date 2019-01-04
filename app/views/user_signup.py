from flask_restful import Resource
from flask import request
from ..models.models import User


class SignUp(Resource):
  def post(self):
    user_data = request.get_json()
    username = user_data.get('username', None)
    email =  user_data.get('email', None)
    password = user_data.get('password', None)
    if password is None or email is None or username is None:
      return {
        "message": "All fields are required. Username, Password and Email"
      }, 400
    user_by_username = User().get_one_where('username', username)
    if user_by_username:
      return {
        "message": "Username has been taken. Kindly choose another"
      }, 400
    
    user_by_email = User().get_one_where('email', email)
    if user_by_email:
      return {
        "message": "Email has been registered. Kindly choose another"
      }, 400

    User().new(username=username, email=email, password=password)
    return {
      "message": "User successfully registered. Proceed to log in.",
      "username": username,
      "email": email
    }, 201


    