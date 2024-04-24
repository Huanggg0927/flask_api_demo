from flask import Flask, request, jsonify
from flask_restful import Api

import pymysql
import pymysql.cursors

import traceback

import jwt
import time

from resources.user import Users, User
from resources.account import Accounts, Account

from server import app
api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(User, '/user/<int:id>')

api.add_resource(Accounts, '/user/<user_id>/accounts')
api.add_resource(Account, '/user/<user_id>/account/<id>')

# @app.errorhandler(Exception)
# def handle_error(error):
#     status_code = 500
#     if type(error).__name__ == "NotFound":
#         status_code = 404
#     elif type(error).__name__ == "TypeError":
#         status_code = 500
    
#     return jsonify({'message': type(error).__name__}),status_code


# @app.before_request
# def auth():
#     token =request.headers.get('auth')
#     user_id = request.get_json()['user_id']
#     encoded_jwt = jwt.encode({'user_id': user_id, 'timestamp': int(time.time())}, 'password', algorithm='HS256')
#     valid_token = jwt.decode(encoded_jwt, 'password', algorithms=['HS256'])
#     print(encoded_jwt)
#     if token == valid_token:
#         pass
#     else :
#         return {
#             "message": "invalid token"
#         }

@app.route('/')
def index():
    return 'Bello home'

@app.route('/user/<user_id>/account/<id>/deposit', methods=['POST'])
def deposit(user_id, id):
    db, cursor, account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] + int(money)
    sql = 'update api.accounts set balance = {} where id = {} and deleted is not True'.format(balance, id)
    response ={}
    try:
        cursor.execute(sql)
        response['message'] = 'success'
    except:
        traceback.print_exc()
        response['message'] = 'failed'

    db.commit()
    db.close()
    return jsonify(response)

@app.route('/user/<user_id>/account/<id>/withdraw', methods=['POST'])
def withdraw(user_id, id):
    db, cursor, account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] - int(money)
    response ={}
    if balance < 0:
        response['message'] = 'money not enough'
        return jsonify(response)
    else :
        sql = 'update api.accounts set balance = {} where id = {} and deleted is not True'.format(balance, id)  
        try:
            cursor.execute(sql)
            response['message'] = 'success'
        except:
            traceback.print_exc()
            response['message'] = 'failed'

        db.commit()
        db.close()
        return jsonify(response)

def get_account(id): 
    db = pymysql.connect(host='localhost', user='root', password='123456', database='api')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """Select * From api.accounts WHERE id = '{}' and deleted is not True""".format(id)
    cursor.execute(sql)
    return db, cursor, cursor.fetchone()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)