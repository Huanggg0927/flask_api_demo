from flask_restful import Resource, reqparse
from flask import jsonify, make_response

import pymysql
import pymysql.cursors

import traceback

from server import db
from models import UserModel

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

class User(Resource):

    def db_init(self):
        db = pymysql.connect(host='localhost', user='root', password='123456', database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    def get(self, id):
        db, cursor = self.db_init()
        sql = """Select * From api.users WHERE id = '{}' and deleted is not True""".format(id)
        cursor.execute(sql)
        user = cursor.fetchone()
        db.close()
        return jsonify({'data': user})
    
    def patch(self, id):
        arg = parser.parse_args()
        user = UserModel.query.filter(id = id, deleted = None).first()
        if arg['name'] != None:
            user.name = arg['name']

        response ={}
        try:
            db.session.commit()
            response['message'] = 'success'
        except:
            traceback.print_exc()
            response['message'] = 'failed'

        return jsonify(response)
    
    def delete(self, id):
        user = UserModel.query.filter(id = id, deleted = None).first()
        
        response ={}
        try:
            db.session.delete(user)
            db.session.commit()
            response['message'] = 'success'
        except:
            traceback.print_exc()
            response['message'] = 'failed'

        return jsonify(response)


class Users(Resource):

    def db_init(self):
        db = pymysql.connect(host='localhost', user='root', password='123456', database='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    def get(self):
        users = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
        return jsonify({'data': list(map(lambda user: user.serialize(), users))})
    
    def post(self):
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'],
            'birth': arg['birth'] or '1900-01-01',
            'note': arg['note']
        }
        response ={}
        status_code = 200
        
        try:
            new_user = UserModel(name=user['name'], gender=user['gender'], birth=user['birth'], note=user['note'])
            db.session.add(new_user)
            db.session.commit()
            response['message'] = 'success'
        except:
            status_code = 400
            traceback.print_exc()
            response['message'] = 'failed'

        return make_response(jsonify(response), status_code)