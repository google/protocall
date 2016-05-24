from protocall.proto import protocall_pb2
from value import value

def plus(left, right):
    result = protocall_pb2.Literal()
    result.integer.value = value(left) + value(right)
    return result

def minus(left, right):
    result = protocall_pb2.Literal()
    result.integer.value = value(left) - value(right)
    return result

def multiply(left, right):
    result = protocall_pb2.Literal()
    result.integer.value = value(left) * value(right)
    return result

def divide(left, right):
    result = protocall_pb2.Literal()
    result.integer.value = value(left) / value(right)
    return result

def equals(left, right):
    result = protocall_pb2.Literal()
    result.boolean.value = value(left) == value(right)
    return result

def less_than(left, right):
    result = protocall_pb2.Literal()
    result.boolean.value = value(left) < value(right)
    return result

def greater_than(left, right):
    result = protocall_pb2.Literal()
    result.boolean.value = value(left) > value(right)
    return result

arithmetic_operators = {
    protocall_pb2.ArithmeticOperator.Op.Value("PLUS"): plus,
    protocall_pb2.ArithmeticOperator.Op.Value("MINUS"): minus,
    protocall_pb2.ArithmeticOperator.Op.Value("MULTIPLY"): multiply,
    protocall_pb2.ArithmeticOperator.Op.Value("DIVIDE"): divide,
    }

comparison_operators = {
    protocall_pb2.ComparisonOperator.Op.Value("EQUALS"): equals,
    protocall_pb2.ComparisonOperator.Op.Value("LESS_THAN"): less_than,
    protocall_pb2.ComparisonOperator.Op.Value("GREATER_THAN"): greater_than,
}
