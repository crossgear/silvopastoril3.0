from flask import flash
from app_web.config.connection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Participante:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.document = data['document']
        self.n_document = data['n_document']
        self.country = data['country']
        self.mail = data['mail']
        self.phone = data['phone']
        self.institution = data['institution']
        self.ocupation = data['ocupation']
        self.payment = data['payment']
        self.participation = data['participation']
        self.conference = data['conference']
        self.english = data['english']
        self.comment = data['comment']
        self.nombre_razon_social = data['nombre_razon_social']
        self.ruc = data['ruc']

    @classmethod
    def getId(cls, data):
        query = "SELECT * FROM silvopastoril.participantes where id = %(id)s;"
        results = connectToMySQL('social').query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        else:
            return None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO silvopastoril.participantes (name, document, n_document, country, city, mail, phone, institution, ocupation, payment, participation, conference, english, comment, nombre_razon_social, ruc) VALUES(%(name)s, %(document)s, %(n_document)s, %(country)s, %(city)s, %(mail)s, %(phone)s, %(institution)s, %(ocupation)s, %(payment)s, %(participation)s, %(conference)s, %(english)s, %(comment)s, %(nombre_razon_social)s, %(ruc)s);"
        mysql = connectToMySQL('silvopastoril')
        result = mysql.query_db(query,data)
        print(result)
        data_participante = {'id': result}
        return cls.getId(data_participante)

    @staticmethod
    def validate_form(participante):
        is_valid = True
        if len(participante['name']) < 2:
            flash("El nombre debe contener al menos 2 caracteres")
            is_valid = False
        if participante['name'] == '':
            flash("Debe proporcionar un nombre")
            is_valid = False
        if participante['documento'] == '':
            flash("Debe Proporcionar un numero de documento")
            is_valid = False
        if not EMAIL_REGEX.match(participante['email']): 
            flash("Email no Valido!!")
            is_valid = False
        return is_valid