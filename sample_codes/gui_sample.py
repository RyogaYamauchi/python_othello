import tkinter


class MyApp1(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        # キャンバスを作成
        self.canvas = tkinter.Canvas(root, bg="green", height=400, width=400)

        # キャンバス上で左っくされたときにイベント発生
        self.canvas.bind('<Button-1>', self.mouse_canvas)
        for i in range(4):
            self.canvas.create_rectangle(0, 400/(i), 400, 400/(i+1), fill='black')
        self.canvas.pack()

        # ラベルを作成
        self.label = tkinter.Label(root, bg="white", height=50, width=300, text="right click me!")
        # 右クリックでイベント発生
        self.label.bind('<Button-3>', self.mouse_label)
        self.label.place(x=200, y=100)
        self.label.pack()

    def mouse_canvas(self, event):
        # キャンバスを左クリックしたときの処理
        print("Left clicked on the canvas -> (" + str(event.x) + ", " + str(event.y) + ")")

    def mouse_label(self, event):
        # ラベルを右クリックしたときの処理
        print("Right clicked on the label-> (" + str(event.x) + ", " + str(event.y) + ")")


root = tkinter.Tk()
root.geometry("400x400")  # Windowのサイズ設定
root.title("Let's Use a Canvvas")  # タイトル作成
app = MyApp1(master=root)
app.mainloop()