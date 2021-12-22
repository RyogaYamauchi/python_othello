# response
# user_id:{user_id},connect:{True}

class ConnectResponse():
    def __init__(self, user_id, is_success, status, errors):
        self.user_id = user_id
        self.is_success = is_success
        self.status = status
        self.errors = errors
