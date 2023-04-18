from flask import render_template, request, redirect, session, flash
from flask_app import app, Bcrypt
from flask_app.models.user import User
from flask_app.models.character import Character
import re

bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    print(request.form)
    if User.get_by_email(request.form):
        flash('Email already registered')
        return redirect('/')
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['user_name'] = data['first_name']
    return redirect('/dashboard')


@app.route('/dashboard')
def dash():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('home.html', characters=Character.get_all())


@app.route('/login', methods=['POST'])
def login():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['user_name'] = user_in_db.first_name
    return redirect("/dashboard")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/createrogue')
def createrogue():
    return render_template('createrogue.html')

@app.route('/createwarrior')
def createwarrior():
    return render_template('createwarrior.html')

@app.route('/createmage')
def createmage():
    return render_template('createmage.html')

@app.route('/examplerogue')
def examplerogue():
    return render_template('examplerogue.html')

@app.route('/examplewarrior')
def examplewarrior():
    return render_template('examplewarrior.html')

@app.route('/examplemage')
def examplemage():
    return render_template('examplemage.html')

@app.route('/createcharacter', methods=['POST'])
def createcharacter():
    Character.save(request.form)
    return redirect('/dashboard')

@app.route('/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    Character.destroy(data)
    return redirect('/dashboard')

@app.route('/edit_d/<int:id>')
def edit_d(id):
    data ={ 
        "id":id
    }
    return render_template("edit_d.html",character=Character.get_one(data))

@app.route('/edit',methods=['POST'])
def update():
    print(request.form)
    data = {"id":id}
    Character.update(request.form)
    return redirect('/dashboard')

@app.route('/inspect/<int:id>')
def inspect(id):
    data ={ 
        "id":id
    }
    return render_template("inspect.html",character=Character.get_one(data))