from flask import flash
from app_web.config.connection import connectToMySQL

class Post:
    def __init__(self,data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.cuerpo = data['cuerpo']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.created_by = data['created_by']
        self.updated_by = data['updated_by']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO silvopastoril.posts (titulo, cuerpo, created_at, updated_at, created_by, updated_by) VALUES(%(titulo)s, %(cuerpo)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0, 0);"
        mysql = connectToMySQL('silvopastoril')
        result = mysql.query_db(query,data)
        print(result)

    @classmethod
    def get_posts(cls):
        query = "SELECT * FROM silvopastoril.posts;"
        results = connectToMySQL('silvopastoril').query_db(query)
        posts = []
        for post in results:
            posts.append( cls(post) )
        return posts

    @classmethod
    def getPostById(cls, data):
        query = "Select * from posts where id = %(id)s;"
        results = connectToMySQL('silvopastoril').query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        else:
            return None
    
    @classmethod
    def update(cls, data):
        query = "UPDATE silvopastoril.posts SET titulo=%(titulo)s, cuerpo=%(cuerpo)s, updated_at=CURRENT_TIMESTAMP, created_by=0, updated_by=0 WHERE id=%(id)s;"
        return connectToMySQL('silvopastoril').query_db(query,data)


    def delete():
        pass