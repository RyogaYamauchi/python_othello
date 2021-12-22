import itertools

import cell_type
import math


class OthelloModel:
    # コンストラクタ
    # 初期値を配置し、最初の画面更新通知を送る
    def __init__(self, view, board_size):
        self.board_size = board_size
        self.view = view
        self.board = [[cell_type.Undefined for j in range(board_size)] for i in range(board_size)]
        center = math.floor(board_size / 2)
        self.board[center - 1][center] = cell_type.PLAYER1
        self.board[center][center - 1] = cell_type.PLAYER1
        self.board[center][center] = cell_type.PLAYER2
        self.board[center - 1][center - 1] = cell_type.PLAYER2
        self.on_changed_board()
        self.is_player_turn = True

    # プレイヤーのターンの開始、入力できた場合はTrue, 入力できなかった場合はFalse
    def do_player_turn(self, x, y):
        succeeded = self.put_player(x, y)
        if succeeded:
            self.judge()
        return succeeded

    # 敵のターンの開始
    def start_com_turn(self):
        self.change_com()
        if self.judge(): # 勝敗がついた場合返す
            return
        self.set_predictive_cells()

    # x,yから状態を変更してviewに通知する
    # 状態が変更できない場合はFalse、できる場合・した場合はTrueを返す
    def put_player(self, x, y):
        cells = self.get_target_all_cells(x, y, cell_type.PLAYER1)
        if len(cells) > 0:
            self.board[x][y] = cell_type.PLAYER1
            for i, j in cells:
                self.board[i][j] = cell_type.PLAYER1
                self.on_changed_board()
            return True
        return False

    # x, yの座標から全ての方向にチェックを行いひっくり返せるcellのlistを返す
    def get_target_all_cells(self, x, y, value):
        # すでに配置されていた場合、[]を返す
        if not (self.board[x][y] == cell_type.Undefined or self.board[x][y] == cell_type.PREDICTIVE):
            return []
        # 空いていた場合候補を調べる
        all_target_cells = []
        for dx in range(-1, 2, 1): # -1, 0, 1
            for dy in range(-1, 2, 1): # -1, 0, 1
                if dx == 0 and dy == 0:
                    continue
                all_target_cells.extend(self.get_target_cells(x, y, dx, dy, value))
        return all_target_cells

    # x, yの座標からdirection_x, direction_yの方向にチェックを行いひっくり返せるcellのlistを返す
    def get_target_cells(self, x, y, direction_x, direction_y, player_or_com):
        opponent_cell_type = cell_type.PLAYER1 if player_or_com == cell_type.PLAYER1 else cell_type.PLAYER2

        target_cell_list = []
        current_x = x
        current_y = y
        while True:
            current_x += direction_x
            current_y += direction_y

            # 範囲外になればひっくり返せる候補なし
            if current_x < 0 or current_x >= self.board_size or current_y < 0 or current_y >= self.board_size:
                break
            # 現在のマスにplayer_or_comが入っていればひっくり返せる候補を返す
            if self.board[current_x][current_y] == player_or_com:
                return target_cell_list
            # 現在のマスが空いていたらひっくり返せる候補なし
            if self.board[current_x][current_y] == cell_type.Undefined or self.board[current_x][current_y] == cell_type.PREDICTIVE:
                break
            # 現在のマスが相手のコマであれば変更可能セルリストに追加してループを継続
            if self.board[current_x][current_y] == opponent_cell_type:
                target_cell_list.append((current_x, current_y))
        return []

    # 盤面の判定を行う
    # PLAYERが勝っていればTrue,　COMが勝っていればFalse
    # 勝敗がついていなければNoneを返す
    def judge(self):
        one_d_array = list(itertools.chain.from_iterable(self.board))
        player_count = len([1 for cell in one_d_array if cell == cell_type.PLAYER1]) #条件付きSUM
        com_count = len([1 for cell in one_d_array if cell == cell_type.COM]) #条件付きSUM

        # 全てのセルが埋まったとき
        if self.are_all_cells_defined():
            text = "プレイヤーの勝利" if player_count > com_count else "コンピュータの勝利"
            self.view.show_result(text)
            return True
        # どちらかが詰んだとき
        if player_count == 0 or com_count == 0:
            text = "プレイヤーの勝利" if player_count > com_count else "コンピュータの勝利"
            self.view.show_result(text)
            return True
        return False

    def are_all_cells_defined(self):
        one_d_array = list(itertools.chain.from_iterable(self.board))
        return all([not (cell == cell_type.Undefined or cell == cell_type.PREDICTIVE) for cell in one_d_array])

    # 全てのcellに対し、入力されたcell_typeの置く場所があるかを判定する
    def can_put(self, player_or_com):
        sum = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                cells = self.get_target_all_cells(i, j, player_or_com)
                count = len(cells)
                sum += count
        return sum > 0

    # 全てのcellに対し、cell_type.PLAYERの置く場所があればcell_type.PREDICTIVEに変換する
    def set_predictive_cells(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == cell_type.PREDICTIVE:
                    self.board[i][j] = cell_type.Undefined
        target_cells = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                cells = self.get_target_all_cells(i, j, cell_type.PLAYER1)
                if len(cells) > 0:
                    target_cells.append((i, j))
        for x, y in set(target_cells):
            self.board[x][y] = cell_type.PREDICTIVE
        self.on_changed_board()

    # viewへの描画通知
    def on_changed_board(self):
        self.view.update(self.board)
