from protocall.proto import protocall_pb2

def value(literal):
    if isinstance(literal, protocall_pb2.Expression) and literal.HasField("atom"):
        return value(literal.atom.literal)
    elif isinstance(literal, protocall_pb2.Expression) and literal.HasField("arithmetic_operator"):
        return literal.arithmetic_operator
    elif isinstance(literal, protocall_pb2.Expression) and literal.HasField("comparison_operator"):
        return literal.comparison_operator
    elif isinstance(literal, protocall_pb2.Expression) and literal.HasField("expression"):
        return literal.expression
    elif isinstance(literal, protocall_pb2.Literal) and literal.HasField("integer"):
        return literal.integer.value
    elif isinstance(literal, protocall_pb2.Literal) and literal.HasField("string"):
        return literal.string.value
    elif isinstance(literal, protocall_pb2.Literal) and literal.HasField("array"):
        return '[ ' + ", ".join([str(value(element)) for element in literal.array.element]) + ' ]'
    elif isinstance(literal, protocall_pb2.Atom):
        return value(literal.literal)
    else:
        print literal.__class__
        import pdb; pdb.set_trace()
        raise RuntimeError
