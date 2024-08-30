from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flash messages and CSRF protection

# Database URL and engine creation
db_url = "sqlite:///Todo.db"
engine = create_engine(db_url, echo=True)

# Declarative base and session creation
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Define the Todo model
class Todo(Base):
    __tablename__ = 'todos'
    sno = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    desc = Column(String(500), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Create the tables
Base.metadata.create_all(engine)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    session = Session()
    allTodo = session.query(Todo).all()

    if request.method == 'POST':
        title = request.form['title'].strip()
        desc = request.form['desc'].strip()
        if not title or not desc:
            flash('Title and Description are required!', 'danger')
        else:
            try:
                todo = Todo(title=title, desc=desc)
                session.add(todo)
                session.commit()
                flash('Todo added successfully!', 'success')
            except Exception as e:
                session.rollback()
                flash(f'Error adding todo: {e}', 'danger')
            finally:
                allTodo = session.query(Todo).all()
    
    session.close()
    return render_template('index.html', allTodo=allTodo)

@app.route('/show')
def products():
    session = Session()
    allTodo = session.query(Todo).all()
    session.close()
    print(allTodo)
    return 'This is products'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update_todo(sno):
    session = Session()
    todo = session.query(Todo).get(sno)
    if request.method == 'POST':
        title = request.form['title'].strip()
        desc = request.form['desc'].strip()
        if not title or not desc:
            flash('Title and Description are required!', 'danger')
        else:
            try:
                todo.title = title
                todo.desc = desc
                session.commit()
                flash('Todo updated successfully!', 'success')
            except Exception as e:
                session.rollback()
                flash(f'Error updating todo: {e}', 'danger')
            finally:
                session.close()
                return redirect(url_for('hello_world'))

    session.close()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete_todo(sno):
    session = Session()
    todo = session.query(Todo).get(sno)
    try:
        session.delete(todo)
        session.commit()
        flash('Todo deleted successfully!', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error deleting todo: {e}', 'danger')
    finally:
        session.close()
    return redirect(url_for('hello_world'))


if __name__ == "__main__":
    app.run(debug=True, port=8000)