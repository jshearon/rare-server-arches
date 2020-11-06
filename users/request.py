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

    row_exists = db_cursor.fetchone() is not None
    token = 12345
    if row_exists:
      returnObject = {"valid": "valid", "token": token}
    else:
      returnObject = {"invalid":"invalid"}
    return json.dumps(returnObject)

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
      return json.dumps({"valid": "User already Exists"})
    else:
      db_cursor.execute("""
        INSERT INTO users
          (first_name, last_name, display_name, email, created_on)
        VALUES 
          (?, ?, ?, ?, ?)
      """, ( new_user['first_name'], new_user['last_name'], new_user['display_name'], new_user['email'], datetime.now()))

      id = db_cursor.lastrowid
      new_user['id'] = id
      return json.dumps({"valid": "valid"})

def update_user(id, new_user):
  with sqlite3.connect("./db/rare.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
      UPDATE users
      SET first_name = ?, last_name = ?, display_name = ?, email = ?
      WHERE id = ?
    """, ( new_user['first_name'], new_user['last_name'], new_user['display_name'], new_user['email'], id, ))

    rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True

def delete_user(id):
  with sqlite3.connect("./db/rare.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
  
    db_cursor.execute("""
      DELETE FROM users
      WHERE id = ?
      """, ( id, ))
