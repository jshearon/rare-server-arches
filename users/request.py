from datetime import datetime
import sqlite3
import json
from models import User


def get_user_by_id(id):
  with sqlite3.connect("./db/rare.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
    SELECT 
      u.id,
      u.first_name,
      u.last_name,
      u.display_name,
      u.email, 
      u.created_on
    FROM users u
    WHERE u.id = ?
    """, (id, ))

    data = db_cursor.fetchone()

    user = User(data['id'], data['first_name'], data['last_name'],
                            data['display_name'], data['email'], data['created_on'])
    return json.dumps(user.__dict__)

def get_user_by_email(email):
  with sqlite3.connect("./db/rare.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    # Write the SQL query to get the information you want
    db_cursor.execute("""
    SELECT 
      u.id,
      u.first_name,
      u.last_name,
      u.display_name,
      u.email, 
      u.created_on
    FROM users u
    WHERE u.email LIKE ?
    """, ( '%'+email+'%', ))

    data = db_cursor.fetchone()

    user = User(data['id'], data['first_name'], data['last_name'], 
      data['display_name'], data['email'], data['created_on'])
    return json.dumps(user.__dict__)

def create_new_user(new_user):
  with sqlite3.connect("./db/rare.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
    SELECT 
      *
    FROM users u
    WHERE u.email LIKE ?
    """, ( '%'+new_user['email']+'%', ))

    row_exists = db_cursor.fetchone() is not None
    
    if row_exists: 
      return {"userAlreadyExists": True}
    else:
      db_cursor.execute("""
        INSERT INTO users
          (first_name, last_name, display_name, email, created_on)
        VALUES 
          (?, ?, ?, ?, ?)
      """, ( new_user['first_name'], new_user['last_name'], new_user['display_name'], new_user['email'], datetime.now()))

      id = db_cursor.lastrowid
      new_user['id'] = id
      return json.dumps(new_user)

def update_entry(id, new_user):
  with sqlite3.connect("./db/dailyjournal.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
      UPDATE entries
      SET concept = ?, entry = ?, date = ?, moodId = ?
      WHERE id = ?
    """, ( new_user['concept'], new_user['entry'], new_user['date'], new_user['moodId'], id, ))

    rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True

def delete_entry(id):
  with sqlite3.connect("./db/dailyjournal.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
  
    db_cursor.execute("""
      DELETE FROM entries
      WHERE id = ?
      """, ( id, ))