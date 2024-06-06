from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    
with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)

# to be added to your existing app.py

#create the route for the api
@app.route('/api/tasks', methods=['GET'])

#function for the api route, it's responsible for handling the GET requests to the '/api/tasks'.
def get_tasks():
        #---pseudo code---
        #Retrieve all tasks from the database ordered by creation date
    tasks = Todo.query.order_by(Todo.date_created).all()
        #Initialize an empty list named task_list
    task_list = []
        #For each task in the retrieved tasks
    for i in tasks:
        #Format task information into a dictionary with keys 'id', 'content', and 'date_created'
        #Append the formatted dictionary to the task_list
        task_list.append({"id": Todo.query.get_or_404(id[i]), 
                          "content": request.form['content'],
                          "date_created": Todo.date_created()})
        #Convert the task_list to JSON format using jsonify
        #Return the JSON response containing the task_list 
    return jsonify(task_list)

            
        