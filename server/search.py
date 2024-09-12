from flask_restful import Resource, reqparse, request
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
class searchBook(Resource):
    
    def get(self):
        query = request.args.get('query')
        filter = request.args.get('filter')
        if query:
            print(query)
            search_results = None
            if filter == 'name':
                search_results = db.session.query(Book).filter(Book.name.ilike(f'%{query}%')).all()
            elif filter == 'section':
                search_results = db.session.query(Book).filter(Book.section.ilike(f'%{query}%')).all()
            elif filter =='author' :                 
                search_results = db.session.query(Book).filter(Book.author.ilike(f'%{query}%')).all()
            search_results_json = [
                {
                    'name': book.name,
                    'author': book.author,
                    'isbn': book.isbn,
                    'publisher': book.publisher,
                    'pages': book.pages,
                    'edition': book.edition,
                    'section': book.section,

                }
                for book in search_results
            ]
            return jsonify(search_results_json)
        else:
            return None