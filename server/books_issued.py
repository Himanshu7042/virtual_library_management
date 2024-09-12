from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from flask import request
import datetime

class issuedBook(Resource):
    @jwt_required()
    def __init__(self) :
        self.username = get_jwt_identity()
    @jwt_required()
    def get(self):
        status_code = request.args.get('status_code', None)
        username = request.args.get('username', None)
        # status_code = request.args.get('status_code')
        if username == 'Admin':
           return Book_issue.filter_by_stauts_code(username=None, status_code=status_code)
        return Book_issue.filter_by_stauts_code(username=username, status_code=status_code)
    
    @jwt_required()
    def put(self, id):
        if self.username == 'Admin' : 
            book = Book_issue.query.filter_by(id=id).first()
        else : 
            book = Book_issue.query.filter_by(username=self.username,id=id).first()
        returnParser = reqparse.RequestParser()
        returnParser.add_argument('status_code')
        
        args = returnParser.parse_args()
        print(args)
        book.status_code = args['status_code']
        book.issue_date = datetime.datetime.now()
        db.session.commit()

        return "status code changed", 200
    
    @jwt_required()
    def delete(self, id):
        book = Book_issue.query.filter_by(username=self.username,id=id).first()
        db.session.delete(book)
        db.session.commit()
        return "request deleted successfully", 200
    