import os

import psycopg2
from flask import session, redirect, url_for, request, flash, render_template
from app import app
from app.models import query_db, execute_db
from functools import wraps
import datetime
import bcrypt

salt = os.getenv('SALT').encode('utf-8')
def auth_user(user):
    session['logged_in'] = True
    session['user_id'] = user['id']
    session['username'] = user['username']
    flash(f'Hello, {user["username"]}!')


def get_current_user():
    if session.get('logged_in'):
        return query_db('SELECT * FROM users WHERE id = %s', [session['user_id']], one=True)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/join/', methods=['GET', 'POST'])
def join():
    if request.method == 'POST' and request.form['username']:
        try:
            password = request.form['password']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            execute_db("""
                INSERT INTO users (username, password, email, join_date)
                VALUES (%s, %s, %s, %s)
            """, [
                request.form['username'],
                hashed_password.decode('utf-8'),
                request.form['email'],
                datetime.datetime.now()
            ])
            user = query_db('SELECT * FROM users WHERE username = %s', [request.form['username']], one=True)
            auth_user(user)
            return redirect(url_for('index'))
        except psycopg2.IntegrityError:
            flash('Username is already taken!')
    return render_template('join.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form['username']:
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        user = query_db("""
            SELECT * FROM users 
            WHERE username = %s AND password = %s
        """, [
            request.form['username'], str(hashed_password)], one=True)

        if user:
            auth_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!')
    return render_template('login.html')


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('Logged out')
    return redirect(url_for('index'))
