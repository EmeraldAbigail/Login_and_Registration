from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask_app import app
from flask import flash

# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User: 
    db = "login_and_registration"
    def __init__(self, data): #data is a dictionary { key: value }
        self.id = data['id']
        self.first_name= data['first_name']
        self.last_name = data['last_name']
        self.email_address = data['email_address']
        self.password = data['password']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        if not results:
            return []
        user = []
        for user in results:
            users.append(cls(user))
            return users

    @classmethod
    def get_one(cls, id):
        query = "SELECT *FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        user = cls(results [0])
        return user


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email_address = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if not result:
            return None
        return cls(result[0])


    @classmethod
    def add(cls, data):
        query = "INSERT INTO users (first_name, last_name, email_address, password) VALUES (%(first_name)s,%(last_name)s,%(email_address)s,%(password)s);"
        user_id = connectToMySQL(cls.db).query_db(query,data)
        return user_id


    @staticmethod
    def validate_user(user):
        is_valid = True
    # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid
        
        # VALIDATE
    @staticmethod
    def validate_login(user):
        is_valid = True
        # checks email
        if len(user['email']) < 3:
            flash("Email must be at least 3 characters", 'login')
            is_valid = False
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'login')
            is_valid = False
        # checks password
        if len(user['password']) < 3:
            flash("Password must be at least 3 characters", 'login')
            is_valid = False
        return is_valid
        
        # checks database for emails in use
    @classmethod
    def check_database(cls, data):
        query = """SELECT * FROM users WHERE email_address = %(email)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    @classmethod
    def get_by_id(cls, data):
        query = """SELECT * FROM users WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results [0]



