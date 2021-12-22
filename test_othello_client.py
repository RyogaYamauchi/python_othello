from scapy.all import *
import lib.waiter as waiter
import lib.sender as sender
import sys
import response_status
import request_and_response

class TestOthelloClient():
    # ユーザIdを作り、サーバに接続しようとする
    def __init__(self, user_id):
        self.user_id = user_id
        print("start connect client :"+str(user_id))
        response = self.connect_to_server()
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


    # サーバに接続する
    def connect_to_server(self):
        print("サーバに接続します...")
        request = request_and_response.ConnectRequest(self.user_id)
        sender.Sender.send(request)
        print("サーバのレスポンスが返ってきました!")
        response = waiter.Waiter.wait(request_and_response.ConnectResponse)
        return response

    def start_game(self, current_player_id):
        print("ゲームスタート!!")
        if self.user_id == current_player_id: # 後攻の場合は相手の手を待つ
            print("先行です")
        else:
            print("後攻です")
            board_request = self.wait_board_update()
        # 手を打つメインループ
        while(True):
            board_request = self.put_to_server()
            print(str(board_request['next_player']))
            if board_request['next_player'] != self.user_id:
                self.wait_board_update()

    def put_to_server(self):
        while(True):
            print("x y = ")
            x, y = input().split()
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

    def wait_board_update(self):
        print("盤面更新待機中...")
        update_request = waiter.Waiter.wait(request_and_response.BoardUpdateRequest)
        time.sleep(random.uniform(0.5, 0.9)) #1秒まって待機状態にする
        update_response = request_and_response.BoardUpdateResponse(self.user_id)
        sender.Sender.send(update_response)
        print("boardの情報が更新されました" + str(update_request['board']))
        return update_request

if __name__ == "__main__":
    # コマンドライン引数でuser_idを指定できるように
    args = sys.argv
    if len(args) > 1:
        user_id = args[1]
    else:
        user_id = random.randint(0, 10000)
    TestOthelloClient(user_id)

