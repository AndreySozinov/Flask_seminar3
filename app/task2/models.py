from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# TODO: Доделать иаблицу ассоциаций авторов с книгами.
association_table = db.Table('association',
                             db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                             db.Column('author_id', db.Integer, db.ForeignKey('author.id')))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer)
    authors = db.relationship('Author', secondary=association_table, backref='books')

    def __repr__(self):
        return f'Book({self.title} Author {self.author.firstname} {self.author.lastname})'


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'Author({self.firstname} {self.lastname})'



