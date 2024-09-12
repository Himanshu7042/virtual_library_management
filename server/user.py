from flask_restful import Resource,reqparse
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity


class allBook(Resource):

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
    


class userInfo(Resource):
    @jwt_required()
    def get(self):
        # Get the username from the JWT payload
        username = get_jwt_identity()
        # Return the username along with the HTTP status code
        return {"username": username}, 200

class requestBook(Resource):
    
    def post(self):
        sectionparser = reqparse.RequestParser()

        sectionparser.add_argument('isbn')
        sectionparser.add_argument('username')
        sectionparser.add_argument('days')
        sectionparser.add_argument('status_code')

        args = sectionparser.parse_args()

        book = Book_issue(isbn=args["isbn"], username=args["username"], days=args["days"], status_code=args["status_code"])
        db.session.add(book)
        db.session.commit()
        return "book requested successfully"

class issuedBook(Resource):
    @jwt_required()
    def __init__(self) :
        self.username = get_jwt_identity()
    @jwt_required()
    def get(self):
        # status_code = request.args.get('status_code')     
        return Book_issue.filter_by_stauts_code(username=self.username, status_code=1), 200
        
         
class userEmail(Resource):
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

class canRequest(Resource):
    @jwt_required()
    def __init__(self) :
        self.username = get_jwt_identity()
    @jwt_required()
    def get(self):
        return True if (len(Book_issue.query.filter_by(username=self.username, status_code = 0).all()) <= 4) else False