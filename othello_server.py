from types import CellType
from scapy.all import *
import time
import request_and_response
import lib.waiter as waiter
import cell_type
import lib.sender as sender
import player
import response_status
import lib.sniffer as sniffer
import lib.serializer as serializer

import threading
import request_and_response

class OthelloServer():
    def __init__(self, users):
        self.players = users
        self.current_turn_player = None
        self.board_size = 8
        self.board = [[cell_type.Undefined for j in range(self.board_size)] for i in range(self.board_size)]
        center = math.floor(self.board_size / 2)
        self.board[center - 1][center] = cell_type.PLAYER1
        self.board[center][center - 1] = cell_type.PLAYER1
        self.board[center][center] = cell_type.PLAYER2
        self.board[center - 1][center - 1] = cell_type.PLAYER2
        self.is_all_player_logined = len(users) == 2
        self.main()

    # サーバのメインループ
    def main(self):
        print("サーバ起動")
        self.debug_setup()
        while(True):
            data = sniffer.Sniffer.sniff()
            request = serializer.Serializer.serialize(data)
            #ログインリクエストが来る
            if(request['class_name']== request_and_response.ConnectRequest.__name__):
                thread = threading.Thread(target=self.connect_request_case, args=(request, ))
                thread.start()
            if(request['class_name']== request_and_response.PutRequest.__name__):
                thread = threading.Thread(target=self.put_request_case, args=(request, ))
                thread.start()

    def debug_setup(self):
        if len(self.players) == 2:
            print("デバッグ起動")
            self.current_turn_player = self.players[0]


    def connect_request_case(self, request):
        # 人数が規定以下だったらログインを試みる
        if len(self.players) < 2:
            user_id = request['user_id']
            self.login_user(user_id)
            time.sleep(random.uniform(0.3,0.9)) #ランダム秒まつ
            response = request_and_response.ConnectResponse(user_id, True, "200", "エラーなし")
            sender.Sender.send(response)
        else:
            response = request_and_response.ConnectResponse(-1, False, response_status.ERROR, "ログインユーザ数が最大です")
            sender.Sender.send(response)
            return

        # ログインした後人数が規定に達していたらゲームスタート
        if len(self.players) == 2:
            self.is_all_player_logined = True
            self.current_turn_player = self.players[0]
            # ゲームがスタートすることをクライアントに通知
            for player in self.players:
                request = request_and_response.GameStartRequest(player.user_id, self.current_turn_player.user_id)
                sender.Sender.send(request)
            remaining_players = [x.user_id for x in self.players]
            player_ids = [x.user_id for x in self.players] # コピーにしたい
            # ゲームスタートのレスポンスを待つ
            while(len(remaining_players) != 0):
                print("ゲーム開始確認のクライアントのレスポンス待ちです...")
                response = waiter.Waiter.wait(request_and_response.GameStartResponse)
                user_id = response['user_id']
                if user_id in remaining_players and user_id in player_ids:
                    print("ゲームスタートの確認が取れました user_id : " + str(user_id))
                    remaining_players.remove(user_id)
            print("ゲームスタート！！")

    # ログインを試みる
    def login_user(self, user_id):
        if(user_id in self.players):
            print("すでにログイン済みのユーザです")
            return
        print("ユーザがログインしました" + str(user_id))
        player_cell_type = cell_type.PLAYER1 if len(self.players)==0 else cell_type.PLAYER2
        self.players.append(player.Player(user_id, player_cell_type))

    def put_request_case(self, request):
            user_id = request['user_id']
            x = request['x']
            y = request['y']
            print("received put data! from: " + str(user_id))
            can_put = self.can_put(x, y, self.current_turn_player.cell_type)
            self.send_put_response(user_id, can_put)
            if not can_put:
                return
            # ターンを変更
            self.change_turn()
            # 盤面をアップデート
            self.put_board(x, y)
            print(str(self.board))
            # 全員に盤面情報を送信
            self.send_all_update_request()

        # putのレスポンスを返す
    def send_put_response(self, user_id, can_put):
        if user_id != self.current_turn_player.user_id: # ログインユーザじゃなかったら無視
            response = request_and_response.PutResponse(user_id, False, response_status.Unauthorized, "ユーザIdが認証されていません")
        elif not can_put:
            response = request_and_response.PutResponse(user_id, False, response_status.CantPut, "指定したセルは置ませんでした")
        else:
            response = request_and_response.PutResponse(user_id, True, response_status.OK, "エラーなし")
        sender.Sender.send(response)

    # requestからユーザ情報、x、yをもとに盤面を更新する
    def put_board(self, x, y):
        self.put_player(x, y, self.current_turn_player.cell_type)

    def can_put(self, x, y, cell_type):
        return len(self.get_target_all_cells(x, y, cell_type)) > 0

    def get_other_player(self):
        if self.current_turn_player == self.players[0]:
            return self.players[1]
        return self.players[0]

    # 状態が変更できない場合はFalse、できる場合・した場合はTrueを返す
    def put_player(self, x, y, cell_type):
        cells = self.get_target_all_cells(x, y, cell_type)
        print(str(cells))
        if len(cells) > 0:
            print("変更 + "+str(cells))
            self.board[x][y] = cell_type
            for i, j in cells:
                self.board[i][j] = cell_type
            return True
        return False

    # ユーザ全員に盤面が変わった通知を送る
    def send_all_update_request(self):
        board = self.board
        next_player_id = self.current_turn_player.user_id
        remaining_players = [x.user_id for x in self.players]
        for user_id in remaining_players:
            request = request_and_response.BoardUpdateRequest(user_id, board, next_player_id)
            sender.Sender.send(request)
        while(len(remaining_players) > 0):
            print("クライアントの盤面更新レスポンス待ちです...")
            response = waiter.Waiter.wait(request_and_response.BoardUpdateResponse)
            response_user_id = response['user_id']
            print("クライアントの盤面更新レスポンスが返ってきました！ user_id : " + str(response_user_id))
            if response_user_id in remaining_players:
                remaining_players.remove(response_user_id)

    def change_turn(self):
        tmp = "ターン変更..."+str(self.current_turn_player.user_id)+"->"
        if self.players[0] == self.current_turn_player:
            self.current_turn_player = self.players[1]
        else:
            self.current_turn_player = self.players[0]
        print(tmp + str(self.current_turn_player.user_id))

    # x, yの座標から全ての方向にチェックを行いひっくり返せるcellのlistを返す
    def get_target_all_cells(self, x, y, player):
        x = int(x)
        y = int(y)
        # すでに配置されていた場合、[]を返す
        if not (self.board[x][y] == cell_type.Undefined):
            return []
        # 空いていた場合候補を調べる
        all_target_cells = []
        for dx in range(-1, 2, 1): # -1, 0, 1
            for dy in range(-1, 2, 1): # -1, 0, 1
                if dx == 0 and dy == 0:
                    continue
                all_target_cells.extend(self.get_target_cells(x, y, dx, dy, player))
        return all_target_cells

        # x, yの座標からdirection_x, direction_yの方向にチェックを行いひっくり返せるcellのlistを返す
    def get_target_cells(self, x, y, direction_x, direction_y, player):
        other_player = self.get_other_player()
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
            if self.board[current_x][current_y] == player:
                return target_cell_list
            # 現在のマスが空いていたらひっくり返せる候補なし
            if self.board[current_x][current_y] == cell_type.Undefined:
                break
            # 現在のマスが相手のコマであれば変更可能セルリストに追加してループを継続
            if self.board[current_x][current_y] == other_player.cell_type:
                target_cell_list.append((current_x, current_y))
        return []

if __name__ == "__main__":
    # コマンドライン引数でuser_idを指定できるように
    args = sys.argv
    users = []
    if len(args) > 1:
        user_id1 = args[1]
        user_id2 = args[2]
        users.append(player.Player(user_id1, cell_type.PLAYER1))
        users.append(player.Player(user_id2, cell_type.PLAYER2))
    OthelloServer(users)

