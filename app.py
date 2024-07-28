from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(500),nullable = False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"  #understand this indepth later 


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        title = request.form.get('title', '')  # Assign a default value if not provided
        desc = request.form.get('desc', '')  # Assign a default value if not provided

        # Create a new Todo instance
        todo = Todo(title=title, desc=desc)

        # Add the new Todo to the database session
        db.session.add(todo)

        # Commit the session to save the changes to the database
        db.session.commit()

    # Retrieve all Todos from the database
    allTodo = Todo.query.all()

    # Render the template with the list of Todos
    return render_template('index.html', allTodo=allTodo)


@app.route('/show')
def show_todo():
        allTodo = Todo.query.all()
        print(allTodo)
        return 'Products Page'

@app.route('/delete/<int:sno>')
def delete(sno):
        todo = Todo.query.filter_by(sno=sno).first()
        if todo is not None:
            db.session.delete(todo)
            db.session.commit()
            return redirect("/")
        else:
             return ("Hello")
        
@app.route('/update/<int:sno>',methods=['GET', 'POST'])
def update(sno):
        if request.method == 'POST':
             title = request.form.get('title', '')
             desc = request.form.get('desc', '')
             todo = Todo.query.filter_by(sno=sno).first()
             todo.title = title
             todo.desc = desc 
             db.session.add(todo)
             db.session.commit()
             return redirect('/')
        todo = Todo.query.filter_by(sno=sno).first()
        return render_template('update.html', todo = todo )
        
        

if __name__ == "__main__":
    app.run(debug = True)
