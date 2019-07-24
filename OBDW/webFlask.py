#!/usr/bin/env python3


from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
import requests
import database

#app.logger.debug('A value for debugging')
#app.logger.warning('A warning occurred (%d apples)', 42)
#app.logger.error('An error occurred')


app = Flask(__name__)


@app.route('/')
def index():
    ''' Function to navigate to either home page or login page 
        Input: None
        Output: rendered template to appropriate page  
    '''
    # if there is an error, get rid of it...
    if 'close_msg' in request.form:
        session.pop('_flashes', None)

    # if you're not logged in send to login page
    if 'username' in session:
        #username = session['username']
        return home()
    # else send to homepage as that user
    else:
        return render_template('login.html')


@app.route('/home')
def home():
    ''' Function...
        Input:
        Output:
    '''
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    ''' Function to login a user 
        Input: None
        Output: index function
    '''
    # get rid of error and return index function
    if 'close_msg' in request.form:
        session.pop('_flashes', None)
        return index()

    # if user tries to login
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = database.Database(r"./OBDW.db")
        db.openDatabase()
        allow = db.isValidUser(username, password)
        db.closeDatabase()
        # check if valid user,if so log them in, else ask them to login again
        if allow:
            session['username'] = username
        else:
            flash('Incorrect username or password, please try again')

        return index()
    # they are trying to create a user
    else:
        return render_template('create.html')


@app.route('/create', methods=['POST'])
def create():
    ''' Function to handel creating a user
        Input: None
        Output: Index function
    '''
    # get rid of the error and return index function
    if 'close_msg' in request.form:
        session.pop('_flashes', None)
        return index()

    # Try to create user
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password2']
    db = database.Database(r"./OBDW.db")
    db.openDatabase()
    isCreated = db.createUser(username, password, password2)
    db.closeDatabase()

    # if sucsessful log them in
    # TODO: return error codes, ir not a symbol, or cap, or numb, or to short, or user already exists, or OK.....instead of bool
    if isCreated:
        flash('New account created successfully.')
        session['username'] = username
        return index()
    else:
        flash('Unsuccessful attempt, please try again')
        return index()


@app.route('/logout')
def logout():
    ''' Function to log a user out
        Input: None
        Output: index function to get to login page 
    '''
    session.pop('username', None)
    #app.config['SHARED'].stop()
    return index()

# hack to use /delete.....TODO: fix it! no hacks allowed
@app.route('/remove')
def remove():
    ''' Function...
        Input:
        Output:
    '''
    return render_template('delete.html')


@app.route('/delete', methods=['POST'])
def delete():
    ''' Function to handel deleting a user
        Input: None
        Output: index function to handel a un/successful delete
    '''
    # get rid of the error and return index function
    if 'close_msg' in request.form:
        session.pop('_flashes', None)
        return index()

    # Try to delete user
    username = session['username']
    password = request.form['password']
    db = database.Database(r"./OBDW.db")
    db.openDatabase()
    uid = db.grabUserID(username, password)
    isDeleted = db.deleteUser(uid, password)
    db.closeDatabase()

    if isDeleted:
        flash('Account deleted successfully :(.')
        session.pop('username', None)
        return index()
    else:
        flash('Unsuccessful attempt, please try again')
        return index()


@app.route('/test')
def test():
    ''' Function ...
        Input: None
        Output: 
    '''
    return render_template('music.html')


@app.route('/music', methods=['POST'])
def music():
    ''' Function ...
        Input: None
        Output: 
    '''
    app.config['SHARED'].record_click()
    return index()
    


@app.errorhandler(404)
def page_not_found(error):
    ''' Function to handle a path not found ie. anything like localhost:port/fakePath
        Input: None
        Output: None
    '''
    return render_template('page_not_found.html'), 404



