import sqlite3
import json

from models.comment import Comment

COMMENTS = [
    Comment(1, "", "", "", "", ""),
    Comment(2, "", "", "", "", ""),
    Comment(3, "", "", "", "", "")
]

def get_all_comments():
    with sqlite3.connect("db/rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.post_id,
            c.subject,
            c.content,
            c.created_on,
            c.is_edited
        FROM comments c
        """)

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            comment = Comment(row['id'], row['post_id'], row['subject'],
                              row['content'], row['created_on'], row['is_edited'])

            comments.append(comment.__dict__)

    return json.dumps(comments)

def get_single_comment(id):
    with sqlite3.connect("db/rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.post_id,
            c.subject,
            c.content,
            c.created_on,
            c.is_edited
        FROM comments c
        WHERE c.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        comment = Comment(data['id'], data['post_id'], data['subject'],
                          data['content'], data['created_on'], data['is_edited'])

    return json.dumps(comment.__dict__)

def get_comment_by_post_id(post_id):
    with sqlite3.connect("rare.db") as conn:
      conn.row_factory = sqlite3.Row
      db_cursor = conn.cursor()

      db_cursor.execute("""
      SELECT
        c.id,
        c.post_id = post_id,
        c.subject = subject,
        c.content = content,
        c.created_on = created_on,
        c.is_edited = is_edited
      FROM comments c
      WHERE c.post_id = ?
      """, ( post_id, ))

      comments = []

      dataset = db_cursor.fetchall()

      for row in dataset:
          comment = Comment(row['id'], row['post_id'], row['subject'],
                            row['content'], row['created_on'], row['is_edited'])
          comments.append(comment.__dict__)

    return json.dumps(comments)
