from models.post import Post
import json
import sqlite3

def get_all_posts():
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.title,
            a.content,
            a.category_id,
            a.publication_date,
            a.user_id,
            a.header_img_url
        FROM posts a
        """)

        # Initialize an empty list to hold all post representations
        posts = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an post instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # post class above.
            post = Post(row['id'], row['title'], row['content'],
                            row['category_id'], row['publication_date'],
                            row['user_id'], row['header_img_url'])

            posts.append(post.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(posts)

# Function with a single parameter
def get_single_post(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.title,
            a.content,
            a.category_id,
            a.publication_date,
            a.user_id,
            a.header_img_url
        FROM posts a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an post instance from the current row
        post = Post(data['id'], data['title'], data['content'],
                            data['category_id'], data['publication_date'],
                            data['user_id'], data['header_img_url'])

        return json.dumps(post.__dict__)

def create_post(new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO posts
            ( title, content, category_id, publication_date, user_id, header_img_url )
        VALUES
            ( ?, ?, ?, ?, ?, ?);
        """, (new_post['title'], new_post['content'],
              new_post['categoryId'], new_post['publicationDate'],
              new_post['userId'], new_post['headerImgUrl'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_post['id'] = id


    return json.dumps(new_post)

def delete_post(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM posts
        WHERE id = ?
        """, (id, ))

def update_post(id, new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE posts
            SET
                title = ?,
                content = ?,
                category_id = ?,
                publication_date = ?,
                user_id = ?,
                header_img_url = ?
        WHERE id = ?
        """, (new_post['title'], new_post['content'],
              new_post['categoryId'], new_post['publicationDate'],
              new_post['userId'], new_post['headerImgUrl'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

