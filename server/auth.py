from flask import session, request
from flask_restful import Resource,reqparse
from flask_jwt_extended import create_access_token
from models import *
import datetime
class userLogin(Resource):
    def post(self):
        loginparser = reqparse.RequestParser()
        loginparser.add_argument('username', type=str)
        loginparser.add_argument('password', type=str)
        args = loginparser.parse_args()

        if args['username'] and args['password']:
            user = User.query.filter_by(username=args['username'],password=args['password']).first()
            if user and user.admin==False :
                access_token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(minutes=240) )
                return {"username":user.username ,"access_token":access_token}, 200
            else :
                return {'message' : 'user not found '}, 404
        else :
            return {'message' : 'username and password are required'}, 404
        

class adminLogin(Resource):
    def post(self):
        print("Something ")
        loginparser = reqparse.RequestParser()
        loginparser.add_argument('username', type=str)
        loginparser.add_argument('password', type=str)
        args = loginparser.parse_args()

        if args['username'] and args['password']:
            user = User.query.filter_by(username=args['username'],password=args['password']).first()
            if user:
                if not user.admin:
                    return {'message' : 'you are not a librarian'}, 400
                access_token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(minutes=240) )
                return {"username":user.username ,"access_token":access_token}, 200
            else :
                return {'message' : 'librarian not found '}, 404
        else :
            return {'message' : 'username and password are required'}, 400

class userSignup(Resource):
    def post(self):
        from sqlalchemy.exc import IntegrityError

        try:
            signUpParser = reqparse.RequestParser()
            signUpParser.add_argument('username', type=str)
            signUpParser.add_argument('password', type=str)
            args = signUpParser.parse_args()
            user = User(username=args['username'],password=args['password'])
            db.session.add(user)

            return {'message': 'signup successful'}, 200
        except:
            db.session.rollback()
            return {'message':'username already exists'}, 400
        finally:
            db.session.commit()
