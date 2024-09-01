from app import app
from app.models import query_db


@app.route('/api/posts/', methods=['GET'])
def get_posts1():
    try:
        results = query_db(
            'SELECT m.id, m.content, m.pub_date, u.username FROM messages m JOIN users u ON m.user_id = u.id ORDER BY m.pub_date DESC')
        return results
    except Exception as e:
        return str(e)


@app.route('/api/users/', methods=['GET'])
def get_users():
    try:
        results = query_db(
            'SELECT username FROM users ORDER BY join_date DESC')
        return results
    except Exception as e:
        return str(e)

@app.route('/api/user/<int:id>', methods=['GET'])
def get_user_info(id):
    try:
        results = query_db(
            'SELECT * FROM users WHERE id= %s', [id])
        return results
    except Exception as e:
        print(str(e))
        return 'error'

@app.route('/api/user/<int:id>/posts', methods=['GET'])
def get_user_posts(id):
    try:
        results = query_db(
            'SELECT users.username, messages.id AS message_id, messages.pub_date FROM "public"."users" JOIN messages ON users.id = messages.user_id WHERE users.id = %s', [id])
        return results
    except Exception as e:
        print(str(e))
        return 'error'


@app.route('/api/post/<int:id>', methods=['GET'])
def get_post_data(id):
    try:
        results = query_db('SELECT id, content, pub_date FROM messages WHERE messages.id = %s', [id])
        print(results)
        return results
    except Exception as e:
        print(str(e))
        return 'error'

