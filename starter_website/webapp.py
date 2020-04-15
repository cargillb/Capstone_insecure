from flask import Flask, render_template, request, redirect, url_for
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)
#webapp = Flask(__name__, static_url_path='/static')

@webapp.route('/')
@webapp.route('/login', methods=['GET', 'POST'])
def login():
    #source: https://realpython.com/introduction-to-flask-part-2-creating-a-login-page/
    error = None
    if request.method == 'POST':
        #Here we will want to check if there are matching username/password combos in the DB
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials, please try again'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@webapp.route('/home/<user_id>')
def home(user_id):
    """
    Route for the home page of a user where all of their to-do lists will be listed
    """
    context = {}  # create context dictionary
    db_connection = connect_to_database()  # connect to db

    query = "SELECT `username` FROM users WHERE `user_id` ='{}'".format(user_id)  # get username
    rtn = execute_query(db_connection, query).fetchall()  # run query
    context = {'user_name': rtn[0][0], 'user_id': user_id}

    query = "SELECT * FROM `lists` WHERE `user_id` ='{}'".format(user_id)  # get list info for a user
    rtn = execute_query(db_connection, query).fetchall()  # run query
    context['rows'] = rtn  # rtn = list data

    return render_template('home.html', context=context)


@webapp.route('/tasks/<list_id>')
def tasks(list_id):
    """
    Route for the tasks page of a user's list where all of the tasks of a to do list are shown
    """
    context = {}  # create context dictionary
    db_connection = connect_to_database()  # connect to db

    query = "SELECT `name`, `description` FROM lists WHERE `list_id` ='{}'".format(list_id)  # get name/desc of list
    rtn = execute_query(db_connection, query).fetchall()  # run query
    context = {'list_name': rtn[0][0], 'list_desc': rtn[0][1]}

    query = "SELECT * FROM `tasks` WHERE `list_id` ='{}'".format(list_id)  # get info of tasks on list
    rtn = execute_query(db_connection, query).fetchall()  # run query
    context['rows'] = rtn  # rtn = tasks data

    return render_template('tasks.html', context=context)
