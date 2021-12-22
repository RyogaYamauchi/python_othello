import math
import othello_model
import othello_view
from scapy.all import *
import lib.waiter as waiter
import lib.sender as sender
import sys
import response_status
import request_and_response
import asyncio
import time


class OthelloController():

    # コンストラクタ
    # 固定の数値の設定を行う
    # view, modelの作成を行う
    def __init__(self, user_id):
        self.user_id = user_id
        self.board_size = 8
        self.canvas_size = 400
        self.view = othello_view.OthelloView(self, self.canvas_size, self.board_size)
        self.model = othello_model.OthelloModel(self.view, self.board_size)
        self.is_player_turn = self.model.is_player_turn
        self.is_put = False
        self.put_x = -1
        self.put_y = -1
        thread = threading.Thread(target=self.login_to_server)
        thread.start()
        self.view.mainloop()

    #サーバへ接続する
    def login_to_server(self):
        print("サーバに接続します... user_id : "+str(self.user_id))
        request = request_and_response.ConnectRequest(self.user_id)
        sender.Sender.send(request)
        print("サーバのレスポンスが返ってきました!")
        response = waiter.Waiter.wait(request_and_response.ConnectResponse)
        if response['is_success']:
            print("サーバとの接続が確認できました")
            is_setuped = False
            while(is_setuped == False):
                print("サーバの応答待ちです...")
                request = waiter.Waiter.wait(request_and_response.GameStartRequest)
                if int(request['user_id']) == user_id:
                    print("サーバの応答が返ってきました")
                    is_setuped = True
                    time.sleep(random.uniform(0.3,0.9)) #ランダム秒まつ
                    response = request_and_response.GameStartResponse(user_id)
                    sender.Sender.send(response)
                current_player_id = request['start_player_id']
            self.start_game(current_player_id)

    # ゲームスタート！
    def start_game(self, current_player_id):
        print("ゲームスタート!!")
        if self.user_id == current_player_id: # 後攻の場合は相手の手を待つ
            print("先行です")
            self.view.set_title("othello あなたは白です user_id : "+str(self.user_id))
        else:
            print("後攻です")
            self.view.set_title("othello あなたは黒です user_id : "+str(self.user_id))
            board_request = self.wait_board_update()
            self.update_view(board_request)
        # 手を打つメインループ
        while(True):
            board_request = self.put_to_server()
            self.update_view(board_request)
            print(str(board_request['next_player']))
            if board_request['next_player'] != self.user_id:
                board_request = self.wait_board_update()
                self.update_view(board_request)

    def update_view(self, request):
        board_data = request['board']
        self.view.update(board_data)


    # サーバに置いた情報を送る
    def put_to_server(self):
        while(True):
            print("入力してください")
            x, y = self.get_input()
            request = request_and_response.PutRequest(self.user_id, x, y)
            sender.Sender.send(request)
            response = waiter.Waiter.wait(request_and_response.PutResponse)
            if response['response_status'] == response_status.OK:
                break
            if response['response_status'] == response_status.CantPut:
                print("指定したセルには置けませんでした")
        print("相手の手を待機中...")
        board_update_request = self.wait_board_update()
        return board_update_request

    # サーバから盤面通知を待つ
    def wait_board_update(self):
        print("盤面更新待機中...")
        update_request = waiter.Waiter.wait(request_and_response.BoardUpdateRequest)
        time.sleep(random.uniform(0.5, 0.9)) #1秒まって待機状態にする
        update_response = request_and_response.BoardUpdateResponse(self.user_id)
        sender.Sender.send(update_response)
        print("boardの情報が更新されました\n" + str(update_request['board']))
        return update_request

    def get_input(self):
        while(not self.is_put):
            time.sleep(0.1)
            print("入力を待っています...")
        self.is_put = False
        return self.put_x, self.put_y

    def wait_input(self, callback):
        while(not self.is_put):
            time.sleep(0.1)
            print("入力を待っています...")
        callback(self.put_x, self.put_y)


    # 左クリックしたときに実行される
    # 入力されたeventに対し、x, y座標を求めmodelにプレイヤーの入力として通知を送る
    # 入力できた場合はCOMの番としてmodelに通知を送る
    # 予測マスを表示する通知をmodelに送る
    def on_click_left(self, event):
        self.is_put = True
        self.is_player_turn = False
        print("Left clicked on the canvas -> (" + str(event.x) + ", " + str(event.y) + ")")
        cell_size = self.canvas_size / self.board_size
        x = math.floor(event.x / cell_size)
        y = math.floor(event.y / cell_size)
        self.put_x = x
        self.put_y = y

if __name__ == "__main__":
    
    # コマンドライン引数でuser_idを指定できるように
    args = sys.argv
    if len(args) > 1:
        user_id = args[1]
    else:
        user_id = random.randint(0, 10000)
    OthelloController(user_id)