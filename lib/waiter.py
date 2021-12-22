from re import S
import lib.serializer as serializer
import lib.sniffer as sniffer
# 特定のコマンドを指定してそのコマンドに合うものだけを待つ
# 特定のコマンドの指定方法は、引数で得られる指定された型の名前
class Waiter():
    def wait(command):
        while(True):
            data = sniffer.Sniffer.sniff()
            serialized = serializer.Serializer.serialize(data)
            if(serialized['class_name']== command.__name__):
                print("# waiter log : "+str(serialized))
                return serialized
