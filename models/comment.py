from datetime import datetime

class Comment():

    def __init__(self, id, post_id, subject, content, created_on, is_edited):
        self.id = id
        self.post_id = post_id
        self.subject = subject
        self.content = content
        self.created_on = created_on
        self.is_edited = is_edited
