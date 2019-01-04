from psycopg2 import connect, ProgrammingError
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

class DB:
  def __init__(self, dsn):
    self.connection = connect(dsn)
    self.cursor = self.connection.cursor()
  
  def commit(self):
    self.connection.commit()
  
  def execute(self, query):
    self.cursor.execute(query)
    try:
      result = self.cursor.fetchall()
    except ProgrammingError:
      result = None
    self.commit()
    return result
  
  def fetch_all():
    return self.cursor.fetchall()
  
  def fetch_one():
    return self.cursor.fetchone()

  def close_session(self):
    self.cursor.close()
    self.connection.close()
  
  def create_tables(self):
    self.execute(User.create_table())
  
  def destroy_tables(self):
    users = "DROP TABLE IF EXISTS users;"
    self.execute(users)


class Table(DB):
  def __init__(self, table_name):
    super().__init__(dsn=current_app.config.get('DATABASE_URL'))
    self.table_name = table_name

  def get_one_where(self, column_name, value, **kwargs):
    extra_conditions = ""
    for column, value in kwargs:
      extra_conditions += f" AND {column}='{value}''"
    query = f"SELECT * FROM {self.table_name} WHERE {column_name}='{value}' {extra_conditions};"
    result = self.execute(query)
    if result:
      self.user_id = result[0][0]
      self.username=result[0][1]
      self.email=result[0][2]
      self.password_hash = result[0][3]
      return self
    return result

class User(Table):
  table_name = 'users'
  def __init__(self):
    super().__init__(User.table_name)

  def new(self, username, email, password=None):
    self.user_id = None
    self.username = username
    self.email = email
    self.password_hash = generate_password_hash(password)
    # import pdb; pdb.set_trace()
    return self
  
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  @staticmethod
  def create_table():
    query = """CREATE TABLE IF NOT EXISTS users(
      user_id serial not null primary key,
      username  varchar not null,
      email  varchar not null,
      password_hash  varchar not null
    );"""
    return query
  
  def save(self):
    query  = f"""INSERT INTO users (username, email, password_hash) VALUES('{self.username}', '{self.email}', '{self.password_hash}') RETURNING user_id;"""
    self.cursor.execute(query)
    self.connection.commit()
    id = self.cursor.fetchone()[0]
    self.user_id = id
    return self
  
  def find_user_by_id(self, id):
    query = f"SELECT * FROM users where user_id={id};"
    self.cursor.execute(query)
    return self.cursor.fetchall()


  @classmethod
  def get_records(cls, column, value, **kwargs):
    cls.get_where(column, value, **kwargs)
    records = cls.fetch_all()
    users = []
    for record in records:
        user = cls.__init__(username=record[1], email=record[2])
        user.user_id = record[0]
        user.password_hash = record[3]
        users.append(user)
    return users

  @classmethod
  def get_user(cls, column, value):
    cls.get_where(column, value)
    user = cls.fetch_one()
    user = cls.__init__(username=user[1], email=user[2])
    user.user_id, user.password_hash = user[0], user[3]
    return user
  

