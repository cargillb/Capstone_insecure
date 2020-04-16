from flask import Flask, render_template, request, redirect, url_for
from db_connector.db_connector import connect_to_database, execute_query
import sys  # to print to stderr
#create the web application
webapp = Flask(__name__)
#webapp = Flask(__name__, static_url_path='/static')


#-------------------------------- Login Routes --------------------------------
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


#-------------------------------- Home (List) Routes --------------------------------
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


@webapp.route('/add_list', methods=['POST'])
def add_list():
    """
    Route to execute query to add lists to db
    """
    db_connection = connect_to_database()
    inputs = request.form.to_dict(flat=True)  # get form inputs from request

    query = "INSERT INTO `lists` (`user_id`, `name`, `description`) VALUES ('{}', \"{}\", \"{}\")".format(inputs['user_id'], inputs['list_name'], inputs['list_desc'])
    execute_query(db_connection, query).fetchall()  # execute query

    return redirect("/home/" + inputs['user_id'])


@webapp.route('/delete_list/<user_id>/<list_id>')
def delete_list(user_id, list_id):
    """
    Route to delete a list
    """
    db_connection = connect_to_database()
    query = "DELETE FROM `lists` WHERE `list_id` = '{}'".format(list_id)
    execute_query(db_connection, query).fetchall()
    return redirect('/home/' + user_id)


#-------------------------------- Task Routes --------------------------------
@webapp.route('/tasks/<list_id>')
def tasks(list_id):
    """
    Route for the tasks page of a user's list where all of the tasks of a to do list are shown
    """
    context = {}  # create context dictionary
    db_connection = connect_to_database()  # connect to db

    query = "SELECT `name`, `description` FROM lists WHERE `list_id` ='{}'".format(list_id)  # get name/desc of list
    rtn = execute_query(db_connection, query).fetchall()  # run query
    context = {'list_name': rtn[0][0], 'list_desc': rtn[0][1], 'list_id': list_id}

    query = "SELECT * FROM `tasks` WHERE `list_id` ='{}'".format(list_id)  # get info of tasks on list
    rtn = execute_query(db_connection, query).fetchall()  # run query
    context['rows'] = rtn  # rtn = tasks data

    return render_template('tasks.html', context=context)


@webapp.route('/add_task', methods=['POST'])
def add_task():
    """
    Route to execute query to add task to db
    """
    db_connection = connect_to_database()
    inputs = request.form.to_dict(flat=True)  # get form inputs from request

    query = "INSERT INTO `tasks` (`list_id`, `dataType_id`, `description`, `completed`) VALUES ('{}', '{}', \"{}\", '{}')".format(inputs['list_id'], inputs['task_type'], inputs['task_desc'], inputs['task_comp'])
    execute_query(db_connection, query).fetchall()  # execute query

    return redirect("/tasks/" + inputs['list_id'])


@webapp.route('/delete_task/<list_id>/<task_id>')
def delete_task(task_id, list_id):
    """
    Route to delete a task
    """
    db_connection = connect_to_database()
    query = "DELETE FROM `tasks` WHERE `task_id` = '{}'".format(task_id)
    execute_query(db_connection, query).fetchall()
    return redirect('/tasks/' + list_id)


@webapp.route('/update_task/<list_id>/<task_id>', methods=['POST', 'GET'])
def update_task(list_id, task_id):
    """
    Display task update form and process any updates using the same function
    """
    db_connection = connect_to_database()

    # display current data
    if request.method == 'GET':
        query = "SELECT * FROM `tasks` WHERE `task_id` ='{}'".format(task_id)  # get info of task
        rtn = execute_query(db_connection, query).fetchall()  # run query
        context = {'task_id': rtn[0][0], 'task_type': rtn[0][2], 'task_desc': rtn[0][3], 'task_comp': rtn[0][4], 'list_id': list_id}
        return render_template('update_task.html', context=context)
    elif request.method == 'POST':
        query = "UPDATE `tasks` SET `dataType_id` = %s, `description` = %s, `completed` = %s WHERE `task_id` = %s"
        data = (request.form['task_type'], request.form['task_desc'], request.form['task_comp'], task_id)
        rtn = execute_query(db_connection, query, data)
        return redirect('/tasks/' + list_id)