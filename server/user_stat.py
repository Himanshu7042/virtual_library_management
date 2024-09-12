from flask_restful import Resource,reqparse
from models import *
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt_identity

class pieData(Resource):
    @jwt_required()
    def __init__(self):
        self.username = get_jwt_identity()
    def get(self):
        if self.username =='Admin':
            section_counts = db.session.query(Book.section, func.count(Book_issue.isbn)).join(Book_issue, Book_issue.isbn == Book.isbn).group_by(Book.section).all()
        else :
            section_counts = db.session.query(Book.section, func.count(Book_issue.isbn)).join(Book_issue, Book_issue.isbn == Book.isbn).filter(Book_issue.username == self.username).group_by(Book.section).all()
        

        section_counts_dict = [{'label': section,'value': count} for section, count in section_counts]

        return section_counts_dict


class barData(Resource):
    @jwt_required()
    def __init__(self):
        self.username = get_jwt_identity()
    def get(self):
        if self.username =='Admin':
            isbn_counts = db.session.query(Book.name, func.count(Book_issue.isbn)).join(Book_issue, Book_issue.isbn == Book.isbn).group_by(Book.name).all()
        else :
            isbn_counts = db.session.query(Book.name, func.count(Book_issue.isbn)).join(Book_issue, Book_issue.isbn == Book.isbn).filter(Book_issue.username == self.username).group_by(Book.name).all()
        

        isbn_counts_dict = [{'label': isbn,'value': count} for isbn, count in isbn_counts]
        
        print(isbn_counts_dict)
        return isbn_counts_dict
