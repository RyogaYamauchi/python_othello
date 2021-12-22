class BoardUpdateRequest():
    def __init__(self, user_id, board, next_player):
        self.user_id = user_id
        self.board = board
        self.next_player = next_player
