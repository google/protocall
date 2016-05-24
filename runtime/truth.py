from protocall.proto import protocall_pb2

def is_true(arg):
    if not arg.literal.HasField("boolean"):
        raise RuntimeError
    return arg.literal.boolean.value


true = protocall_pb2.Boolean()
true.value = True
false = protocall_pb2.Boolean()
false.value = False

literal_true = protocall_pb2.Literal()
literal_true.boolean.CopyFrom(true)
literal_false = protocall_pb2.Literal()
literal_false.boolean.CopyFrom(false)
