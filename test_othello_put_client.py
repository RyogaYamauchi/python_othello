from scapy.all import *
import lib.waiter as waiter
import lib.sender as sender
import sys
import request_and_response

class TestOthelloPutClient():
    # ユーザIdを作り指定したx, yに置こうとする
    def __init__(self, user_id):
        print("start put client :"+str(user_id))
        while(True):
            print("x y = ")
            x, y = input().split()
            response = self.put_to_server(user_id, x, y)
            print(response['user_id'] + "が" +x + " " + y + "におきました")

    def put_to_server(self, user_id, x, y):
        request = request_and_response.PutRequest(user_id, x, y)
        sender.Sender.send(request)
        print("置いたレスポンス待ちです...")
        response = waiter.Waiter.wait(request_and_response.PutResponse)
        print("置いたレスポンスが返ってきました!")
        # 盤面を待つ
        print("盤面更新通知待ちです...")
        update_request = waiter.Waiter.wait(request_and_response.BoardUpdateRequest)
        print("盤面更新通知が来ました！！")
        time.sleep(random.uniform(0.3, 0.9)) #1秒まって待機状態にする
        update_response = request_and_response.BoardUpdateResponse(user_id)
        sender.Sender.send(update_response)
        return response

if __name__ == "__main__":
    # コマンドライン引数でuser_idを指定できるように
    args = sys.argv
    if len(args) > 1:
        user_id = args[1]
    else:
        user_id = random.randint(0, 10000)
    TestOthelloPutClient(user_id)
