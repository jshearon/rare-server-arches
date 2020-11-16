import sqlite3
import json
from models import Tag, PostTag, PostTagJoined


def get_tag_by_id(id):
  with sqlite3.connect("./rare.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
    SELECT 
      t.id,
      t.name
    FROM tags t
    WHERE t.id = ?
    """, (id, ))

    data = db_cursor.fetchone()

    tag = Tag(data['id'], data['name'])
    return json.dumps(tag.__dict__)

def get_tags_by_postId(postId):
  with sqlite3.connect("./rare.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
      SELECT
        p.id,
        t.name,
        p.post_id 
      FROM postTags p
      LEFT JOIN tags t
        ON p.tag_id = t.id 
      WHERE p.post_id = ?
    """, (postId, ))

    tags = []

    dataset = db_cursor.fetchall()

    for row in dataset:
      tag = PostTagJoined(row['id'], row['name'], row['post_id'])
      tags.append(tag.__dict__)
  return json.dumps(tags)

def get_all_tags():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            t.id,
            t.name
        FROM tags t
        """)

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'], row['name'])

            tags.append(tag.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(tags)

def create_new_tag(new_tag):
  with sqlite3.connect("./rare.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
    SELECT 
      *
    FROM tags t
    WHERE t.name = ?
    """, ( new_tag['name'], ))

    row_exists = db_cursor.fetchone() is not None
    
    if row_exists: 
      return json.dumps({"invalid": "Tag already Exists"})
    else:
      db_cursor.execute("""
        INSERT INTO tags
          ( name )
        VALUES 
          ( ? )
      """, ( new_tag['name'], ))

      id = db_cursor.lastrowid
      new_tag['id'] = id
      return json.dumps({"valid": "valid"})

def create_new_post_tag(new_tag):
  with sqlite3.connect("./rare.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
    SELECT 
      *
    FROM postTags t
    WHERE t.post_id = ? AND t.tag_id = ?
    """, ( new_tag['post_id'], new_tag['tag_id']) )

    row_exists = db_cursor.fetchone() is not None
    
    if (row_exists or new_tag['post_id'] == "" or new_tag['tag_id'] == ""):
      return json.dumps({"invalid": "Tag already Exists"})
    else:
      db_cursor.execute("""
        INSERT INTO postTags
          ( post_id, tag_id )
        VALUES 
          ( ?, ? )
      """, ( new_tag['post_id'], new_tag['tag_id'] ))

      id = db_cursor.lastrowid
      new_tag['id'] = id
      return json.dumps({"valid": "valid"})

def update_tag(id, new_tag):
  with sqlite3.connect("./rare.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()

    db_cursor.execute("""
      UPDATE tags
      SET name = ?
      WHERE id = ?
    """, ( new_tag['name'], id, ))

    rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True

def delete_tag(id):
  with sqlite3.connect("./rare.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
  
    db_cursor.execute("""
      DELETE FROM tags
      WHERE id = ?
      """, ( id, ))

def delete_post_tag(id):
  with sqlite3.connect("./rare.db") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
  
    db_cursor.execute("""
      DELETE FROM postTags
      WHERE id = ?
      """, ( id, ))
