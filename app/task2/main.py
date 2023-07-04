from flask import Flask, render_template
from app.task2.models import db, Book, Author

app = Flask(__name__)
app.secret_key=b'jhgmvytjy56r55rjfkur5ece5roti8yb8yy7tktk6rvkt6kuvt'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.route('/')
def index():
    return render_template('base.html')


@app.cli.command('init-db')
def init_db():
    db.create_all()


@app.cli.command('fill-db')
def fill_tables():
    count = 5
    for author in range(1, count + 1):
        new_author = Author(firstname=f'Имя {author}', lastname=f'Фамилия {author}')
        db.session.add(new_author)
    db.session.commit()

    for book in range(1, count ** 2):
        author = Author.query.filter_by(lastname=f'Фамилия {book % count + 1}').first()
        new_book = Book(title=f'Название {book}',
                              year=1910+book,
                              amount=book*27,
                              author=author)
        db.session.add(new_book)
    db.session.commit()


@app.route('/books/')
def all_books():
    books = Book.query.all()
    # books = Book.query.join(Author.books).all()
    context = {
        'title': 'Книги',
        'books': books}
    return render_template('books.html', **context)
