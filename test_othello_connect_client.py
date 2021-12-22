from scapy.all import *
import lib.waiter as waiter
import lib.sender as sender
import sys
import request_and_response

class TestOthelloConnetClient():
    # ユーザIdを作り、サーバに接続しようとする
    def __init__(self, user_id):
        print("start connect client :"+str(user_id))
        response = self.connect_to_server(user_id)
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
        print("接続完了 ゲームスタート")

    # サーバに接続する
    def connect_to_server(self, user_id):
        request = request_and_response.ConnectRequest(user_id)
        sender.Sender.send(request)
        response = waiter.Waiter.wait(request_and_response.ConnectResponse)
        return response

if __name__ == "__main__":
    # コマンドライン引数でuser_idを指定できるように
    args = sys.argv
    if len(args) > 1:
        user_id = args[1]
    else:
        user_id = random.randint(0, 10000)
    TestOthelloConnetClient(user_id)
