from types import SimpleNamespace

class Deserializer():
    # 引数で指定されたインスタンスの持つフィールドをstringにして返す
    # オブジェクトの判定はクラスネームを使う
    def deserialize(data):
        data.class_name =type(data).__name__
        return str(data.__dict__)
