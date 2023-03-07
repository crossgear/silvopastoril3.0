from flask import flash
from app_web.config.connection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id = data['id']
        self.username =data['username']
        self.password =data['password']
        self.email = data['email']
        self.is_superuser = data['is_superuser']

    @classmethod
    def getId(cls, data):
        query = "Select * from silvopastoril.users where id = %(id)s;"
        results = connectToMySQL('silvopastoril').query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        else:
            return None

    @classmethod
    def save_user(cls,data):
        query="INSERT INTO silvopastoril.users(username, password, email, is_superuser)VALUES(%(username)s, %(passw)s, %(email)s, 0);"
        mysql = connectToMySQL('silvopastoril')
        result = mysql.query_db(query,data)
        print(result)
        data_usuario = {'id': result}
        return cls.getId(data_usuario)

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM silvopastoril.users;"
        results = connectToMySQL('silvopastoril').query_db(query)
        users = []
        for usrs in results:
            users.append( cls(usrs) )
        return users
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM silvopastoril.users WHERE email = %(email)s;"
        result = connectToMySQL("silvopastoril").query_db(query,data)
        # no se encontró un usuario coincidente
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @staticmethod
    def validar_usuario(registro):
        correo={
            "email":registro['email']
        }

        is_valid = True # asumimos que esto es true
        if len(registro['username']) < 3:
            flash("Nombre debe contener al menos 3 caracteres")
            is_valid = False
        
        if len(registro['password']) < 8:
            flash("Password debe tener al menos 8 caracteres")
            is_valid = False

        if not EMAIL_REGEX.match(correo['email']):
            flash("Email no valido")
            is_valid = False

        elif User.get_by_email(correo):
            flash("Email ya existente")
            is_valid = False

        return is_valid