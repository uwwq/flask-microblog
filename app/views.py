import datetime

from flask import render_template, request, flash, session

from app import app
from app.auth import login_required
from app.models import execute_db


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create/', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            execute_db('INSERT INTO messages (user_id, content, pub_date) VALUES (%s, %s, %s)', [
                session['user_id'], content, datetime.datetime.now()
            ])
            flash('Message was posted')
    return render_template('index.html')
