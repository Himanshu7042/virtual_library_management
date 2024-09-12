from flask import session, request, abort
from flask_restful import Resource,reqparse
from sqlalchemy import distinct
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity
class adminBook(Resource):
    
    def post(self):
        sectionparser = reqparse.RequestParser()
        sectionparser.add_argument('name')
        sectionparser.add_argument('author')
        sectionparser.add_argument('isbn')
        sectionparser.add_argument('publisher')
        sectionparser.add_argument('pages')
        sectionparser.add_argument('edition')
        sectionparser.add_argument('section')

        args = sectionparser.parse_args()

        # Check if ISBN is already in the database
        existing_book = Book.query.filter_by(isbn=args["isbn"]).first()
        if existing_book:
            abort(409, description="ISBN number should be unique.")

        book = Book(name=args["name"], author=args["author"], isbn=args["isbn"], publisher=args["publisher"], pages=args["pages"], edition=args["edition"], section=args["section"])
        db.session.add(book)
        db.session.commit()
        return "book added successfully"
    def put(self, isbn):
        sectionparser = reqparse.RequestParser()
        sectionparser.add_argument('name')
        sectionparser.add_argument('author')
        sectionparser.add_argument('isbn')
        sectionparser.add_argument('publisher')
        sectionparser.add_argument('pages')
        sectionparser.add_argument('edition')
        sectionparser.add_argument('section')
        args = sectionparser.parse_args()
        book = Book.query.filter_by(isbn = isbn).first()
        book.name = args['name']
        book.author = args['author']
        book.publisher = args['publisher']
        book.pages = args['pages']
        book.edition = args['edition']
        db.session.commit()

        return "edited successfully", 200
    def get(self):
        result = Book.query.group_by(Book.section).all()

        section_books = {}

        # Iterate through each section in the result
        for section in result:
            # Get the section name
            section_name = section.section
            # Retrieve all books belonging to the current section
            books = Book.query.filter_by(section=section_name).all()
            # Create a list of dictionaries for each book
            book_list = [{ 'name': book.name,
                        'author': book.author,
                        'isbn': book.isbn,
                        'publisher': book.publisher,
                        'pages': book.pages,
                        'edition': book.edition,
                        'section': book.section } for book in books]
            # Add the section and its corresponding list of books to the dictionary
            section_books[section_name] = book_list
        return section_books
    
    def delete(self, isbn):
        book = Book.query.filter_by(isbn = isbn ).first()
        db.session.delete(book)
        db.session.commit()
        return "deleted successfully", 200
        


class adminSections(Resource):

    def get(self):
        sections = Book.query.with_entities(Book.section).distinct().all()

        return {"sections": [sectiion[0] for sectiion in sections]}
    def put(self, oldname):
        parser = reqparse.RequestParser()
        parser.add_argument('newName')
        args = parser.parse_args()

        section =Book.query.filter_by(section=oldname).all()
        for x in section:
            x.section = args['newName']
        db.session.commit()
        return "section edited successfully",200
    def delete(self, oldname):
        section = Book.query.filter_by(section=oldname).all()
        for x in section:
            db.session.delete(x)
        db.session.commit()

        return "section deleted successfully",200
class adminInfo(Resource):
    @jwt_required()
    def get(self):
        # Get the username from the JWT payload
        username = get_jwt_identity()
        # Return the username along with the HTTP status code
        return {"username": username}, 200

class adminEmail(Resource):
    @jwt_required()
    def __init__(self) :
        self.username = get_jwt_identity()
    @jwt_required()
    def put(self):
        emailparser = reqparse.RequestParser()
        emailparser.add_argument('email')
        args = emailparser.parse_args()
        user = User.query.filter_by(username=self.username).first()
        user.email = args['email'] 
        db.session.commit()
        return "email added successfully",200
