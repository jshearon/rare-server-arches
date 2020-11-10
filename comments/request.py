import sqlite3
import json

from models.comment import Comment

def get_all_comments():
    with sqlite3.connect("./rare.db") as conn:

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

def create_comment(new_comment):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO comments
            ( post_id, subject, content, created_on, is_edited )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_comment['post_id'], new_comment['subject'],
              new_comment['content'], new_comment['created_on'],
              new_comment['is_edited'], ))

        id = db_cursor.lastrowid

        new_comment['id'] = id

    return json.dumps(new_comment)

def delete_comment(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM comments
        WHERE id = ?
        """, (id, ))
