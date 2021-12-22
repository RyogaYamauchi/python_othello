import math

import othello_model
import othello_view


class OthelloController():

    # コンストラクタ
    # 固定の数値の設定を行う
    # view, modelの作成を行う
    def __init__(self):
        self.board_size = 8
        self.canvas_size = 400
        self.view = othello_view.OthelloView(self, self.canvas_size, self.board_size)
        self.model = othello_model.OthelloModel(self.view, self.board_size)
        self.is_player_turn = self.model.is_player_turn
        self.view.mainloop()

    # 左クリックしたときに実行される
    # 入力されたeventに対し、x, y座標を求めmodelにプレイヤーの入力として通知を送る
    # 入力できた場合はCOMの番としてmodelに通知を送る
    # 予測マスを表示する通知をmodelに送る
    def on_click_left(self, event):
        if not self.is_player_turn: # 自分のターンかどうか
            return
        self.is_player_turn = False
        print("Left clicked on the canvas -> (" + str(event.x) + ", " + str(event.y) + ")")
        cell_size = self.canvas_size / self.board_size
        x = math.floor(event.x / cell_size)
        y = math.floor(event.y / cell_size)
        print("x : " + str(x) + ", y : " + str(y))
        changed = self.model.do_player_turn(x, y) # 置いてみる
        if not changed: # 置けないところをクリックした場合
            self.is_player_turn = True
            return
        # thinkerというGUIライブラリは、time.sleepだとmainループを止めてしまうためアニメーションができない模様
        # 代わりにafterというメソッドが用意されていて、コールバック(関数のアドレス)を渡すと指定した秒数後に実行してくれる
        self.view.root.after(1000, lambda: self.turn_over()) #命名に関して：プレイヤーが交代した

    def turn_over(self):
        self.model.start_com_turn()
        self.is_player_turn = True

if __name__ == "__main__":
    OthelloController()
