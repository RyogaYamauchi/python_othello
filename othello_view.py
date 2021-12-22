import tkinter
import cell_type


class OthelloView(tkinter.Frame):

    # コンストラクタ
    # canvasの作成、ボードの描画などを行う
    def __init__(self, controller, canvas_size, board_size):
        self.controller = controller
        self.root = tkinter.Tk()
        self.canvas_size = canvas_size  # キャンバスの大きさ
        self.board_size = board_size
        self.canvas = tkinter.Canvas(self.root, bg="green", height=canvas_size, width=canvas_size)
        self.root.geometry(f"{canvas_size}x{canvas_size}")  # Windowのサイズ設定
        self.root.title("Othello game")  # タイトル作成
        super().__init__(self.root)
        self.render_board()
        self.set_binds()

    def set_title(self, title):
        self.root.title(title)

    # ボードの画面描画
    def render_board(self):
        self.canvas.create_rectangle(0, 0, self.canvas_size, self.canvas_size, fill="#4db56a")
        one_size = self.canvas_size / self.board_size
        for i in range(1, self.board_size):
            pos = i * one_size
            self.canvas.create_line(0, pos, self.canvas_size, pos)
        for i in range(1, self.board_size):
            pos = i * one_size
            self.canvas.create_line(pos, 0, pos, self.canvas_size)
        self.canvas.pack()

    # 入力したときのコールバックの設定
    def set_binds(self):
        self.canvas.bind('<Button-1>', self.controller.on_click_left)

    # セルを含んだ盤面の描画
    def update(self, board):
        self.render_board()
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.render_cell(i, j, board[i][j])
        self.canvas.pack() #描画

    # 画面中央に勝敗の結果を表示する
    def show_result(self, text):
        pos = self.canvas_size / 2
        self.canvas.create_text(pos, pos, text=text, font=('FixedSys', 30), fill="#ff0000")

    # セルを描画する
    def render_cell(self, x, y, value):
        one_size = self.canvas_size / self.board_size
        x_pos = one_size * x
        y_pos = one_size * y
        if value != cell_type.Undefined:
            if value == cell_type.PLAYER1:
                color = '#ffffff'
            if value == cell_type.PLAYER2:
                color = '#000000'
            if value == cell_type.PREDICTIVE:
                color = '#fffacd'
                one_size /= 2
                x_pos += one_size / 2
                y_pos += one_size / 2
            self.canvas.create_oval(x_pos, y_pos, x_pos + one_size, y_pos + one_size, fill=color)

