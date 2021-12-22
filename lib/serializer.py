import ast

class Serializer():
    def serialize(instance):
        return ast.literal_eval(instance)
