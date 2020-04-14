from flask import Flask, render_template, request, redirect, url_for
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

@webapp.route('/')
@webapp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #Here we will want to check if there are matching username/password combos in the DB
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error = error)

#def list_lists(user_id):        #home page displays a list of users lists
#    db_connection = connect_to_database
#    query = "SELECT 'name' FROM lists WHERE user_id = '{user_id}'"
#    execute_query(db_connection, query).fetchall()
#    context = {

def login():
    return render_template('login.html')

#def home_page():
#    context = {'list_lists(user_id)':)