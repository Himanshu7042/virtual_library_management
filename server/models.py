from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    username = db.Column(db.String(50),primary_key=True)
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean, default= False)
    email = db.Column(db.String(50))

class Book(db.Model):
    name = db.Column(db.String(150))
    author = db.Column(db.String(150))
    isbn = db.Column(db.String(150), primary_key=True)
    publisher = db.Column(db.String(150))
    pages = db.Column(db.Integer)
    edition = db.Column(db.Integer)
    section = db.Column(db.String(150))
    def to_dict(self):
        return {
            'name' : self.name,
            'author' : self.author,
            'isbn': self.isbn,
            'publisher': self.publisher,
            'pages': self.pages,
            'edition': self.edition,
            'section': self.section
        }

class Book_issue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(50), db.ForeignKey('book.isbn'))
    username = db.Column(db.String(50), db.ForeignKey('user.username'))
    days = db.Column(db.Integer)
    status_code = db.Column(db.Integer)
    
    def to_dict(self):
        book = Book.query.filter_by(isbn = self.isbn).first()
        return {
            'id': self.id,
            'isbn': self.isbn,
            'username': self.username,
            'days': self.days,
            'status_code':self.status_code,
            'book' : book.to_dict()
        }
    def filter_by_stauts_code(username, status_code):
        if username == None :
            books = Book_issue.query.filter_by( status_code = status_code).all()
        else :
            books = Book_issue.query.filter_by(username=username, status_code = status_code).all()
        return [ book.to_dict() for book in books ], 200