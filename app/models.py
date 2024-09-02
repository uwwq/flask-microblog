import psycopg2

from app import app


def connect_db():
    return psycopg2.connect(**app.config['DATABASE'])

def init_db():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    email VARCHAR(50),
                    join_date TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    content TEXT NOT NULL,
                    pub_date TIMESTAMP
                );

                CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
                CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id);
                CREATE INDEX IF NOT EXISTS idx_messages_pub_date ON messages(pub_date);
            """)

def query_db(query, args=(), one=False):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(query, args)
    col_names = [desc[0] for desc in cur.description]
    rv = cur.fetchall()
    result = [dict(zip(col_names, row)) for row in rv]
    cur.close()
    return (result[0] if result else None) if one else result

def execute_db(query, args=()):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()
    conn.close()