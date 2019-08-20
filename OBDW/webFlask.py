from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import requests
import database
import time
import os

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
    if 'userID' in session:
        return home()

    # else send to homepage as that user
    else:
        return render_template('login.html')


@app.route('/home')
def home():
    ''' Function to render the initial home page
        Input:  None
        Output: None
    '''
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    ''' Function to login a user (if the password and username are valid)
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
        # see if they are really a user
        app.config['SHARED'].record_login(username, password)
        time.sleep(0.1)
        allow = app.config['SHARED'].currentUser
        # check if valid user,if so log them in, else ask them to login again
        if allow is not None:
            # store user is in the session
            session['userID'] = allow
            app.config['SHARED'].record_refresh(session['userID'])
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

    app.config['SHARED'].record_create(username, password, password2)
    time.sleep(0.1)
    created = app.config['SHARED'].currentUser

    # If sucsessful log them in
    # TODO: return error codes, or not a symbol, or cap, or numb, or to short, or user already exists, or OK.....instead of bool
    if created:
        flash('New account created successfully.')
        session['userID'] = created
        
    else:
        flash('Unsuccessful attempt, please try again')
    return index()


@app.route('/logout')
def logout():
    ''' Function to log a user out
        Input: None
        Output: index function to get to login page 
    '''
    session.pop('userID', None)
    app.config['SHARED'].currentUser = None
    return index()


@app.route('/remove')
def remove():
    ''' Function to render delete html page
        Input:  None
        Output: render_template
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
    uid = session['userID']
    password = request.form['password']
    app.config['SHARED'].record_delete(uid, password)
    time.sleep(0.3)
    deleted = app.config['SHARED'].currentUser

    if deleted is None:
        flash('Account deleted successfully :(.')
        session.pop('userID', None)
        return index()
    else:
        flash('Unsuccessful attempt, please try again')
        return index()


@app.route('/recommend')
def recommend():
    ''' Function to load recomendation list and render music html page
        Input: None
        Output: render_template
    ''' 
    recommendation = app.config['SHARED'].recommenList 
    print('grab list')
    return render_template('music.html', recommendation=recommendation)

@app.route('/music', methods=['POST', 'GET', 'PUT'])
def music():
    ''' Function to handel difffernt calls to and from the music page 
        Input: None
        Output: recommend function
    '''
    print('here')
    if request.method == 'POST':
        waiting = True
        while waiting:
            if app.config['SHARED'].loading:
                time.sleep(0.5)
                print('still waiting')
            else:
                print('unflashed')
                session.pop('_flashes', None)
                waiting=False

        # save the ratings
        if request.form['music'] == "Save Ratings":
            ratedSongs = []
            for idx in range(10):
                song = request.form.get('r'+str(idx)+'s', None)
                rating = request.form.get('r'+str(idx), None)
                if rating is not None:
                    app.config['SHARED'].recommenList[idx][5] = int(rating)
                    ratedSongs.append([session['userID'], song, int(rating)])
            app.config['SHARED'].record_user_rating(ratedSongs)
            time.sleep(0.3)
            pass

        # Refresh without reloading
        elif request.form['music'] == "Cancel":
            pass

        # This means they want the GUI
        elif request.form['music'] == "Configure app":
            app.config['SHARED'].record_click(session['userID'])
            app.config['SHARED'].loading = True
            time.sleep(0.1)
            flash("Loading...")
            print('flashed')

        # Refresh the page
        else:
            app.config['SHARED'].record_refresh(session['userID'])
            time.sleep(0.8)
                 
    return recommend()


@app.route('/loading')
def loading():
    ''' Function to handel reloading the music page with new recommendations 
        Input: None
        Output: render_template or recommend function
    '''
    if app.config['SHARED'].load:
        return render_template('loading.html')
    else:
        session.pop('_flashes', None)
        return recommend()


@app.route('/contact')
def contact():
    ''' Function to render the contact html page 
        Input:  None
        Output: render_template
    '''
    return render_template('contact.html')


@app.route('/about')
def about():
    ''' Function to render the contact html page
        Input:  None
        Output: render_template
    '''
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(error):
    ''' Function to handle a path not found ie. anything like localhost:port/fakePath
        Input: None
        Output: None
    '''
    return render_template('page_not_found.html'), 404
