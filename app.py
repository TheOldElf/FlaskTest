from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'  

db = SQLAlchemy(app)


# Маршрут для главной страницы
@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('login'))

# Модель книги
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    publication_date = db.Column(db.String(20), nullable=False)

    def __init__(self, title, author, publication_date):
        self.title = title
        self.author = author
        self.publication_date = publication_date


# Маршрут для авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'user' and password == 'user':
            return redirect(url_for('books_list'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


# Маршрут для просмотра списка книг
@app.route('/books', methods=['GET'])
def books_list():
    books = Book.query.all()
    return render_template('books.html', books=books)


# Маршрут для добавления книги
@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_date = request.form['publication_date']

        book = Book(title, author, publication_date)
        db.session.add(book)
        db.session.commit()

        return redirect(url_for('books_list'))

    return render_template('add_book.html')


# Маршрут для удаления книги
@app.route('/books/delete/<int:book_id>', methods=['GET'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('books_list'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)