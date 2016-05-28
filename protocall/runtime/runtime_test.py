# Copyright 2016 Google Inc. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for protocall.runtime.runtime."""

import unittest

from google.protobuf import text_format

from protocall.proto import protocall_pb2
from protocall.runtime.vm import Protocall
from protocall.runtime import dump

from protocall.runtime.truth import true, false, literal_true, literal_false
from protocall.runtime.symbols import Symbols


def create_expression():
    e = protocall_pb2.Expression()
    e.arithmetic_operator.operator = protocall_pb2.ArithmeticOperator.Op.Value("MULTIPLY")
    e.arithmetic_operator.left.atom.literal.integer.value = 9
    e2 = e.arithmetic_operator.right
    e2.arithmetic_operator.operator = protocall_pb2.ArithmeticOperator.Op.Value("PLUS")
    e2.arithmetic_operator.left.atom.field.component.add().name = 'xyz'
    e2.arithmetic_operator.right.atom.literal.integer.value = 5
    return e

def test_evaluate():
    expression = create_expression()
    a = protocall_pb2.Atom()
    a.literal.integer.value = 5
    symbols = Symbols({'xyz': a})
    pr = Protocall(symbols)
    print "Expression:"
    print dump.dump_expression(expression)
    result = pr.evaluate(expression)
    print "Result:"
    print result
    return result

def test_evaluate_array():
    expression = create_expression()
    a = expression.atom
    array = a.literal.array
    element = array.element.add()
    op = element.arithmetic_operator
    op.left.atom.field.component.add().name = "x"
    op.right.atom.literal.integer.value = 5
    op.operator = protocall_pb2.ArithmeticOperator.Op.Value("PLUS")
    atom = protocall_pb2.Atom()
    atom.literal.integer.value = 5
    symbols = Symbols({'x': atom})

    pr = Protocall(symbols)
    print "Expression:"
    print dump.dump_expression(expression)
    result = pr.evaluate(expression)
    print "Result:"
    print result
    return result

def create_block():
    p = protocall_pb2.Block()

    s = p.statement.add()
    s.assignment.field.component.add().name = 'x'
    e = s.assignment.expression
    e.arithmetic_operator.left.atom.literal.integer.value = 7
    e.arithmetic_operator.right.atom.literal.integer.value = 5
    e.arithmetic_operator.operator = protocall_pb2.ArithmeticOperator.Op.Value("PLUS")

    s2 = p.statement.add()
    e = s2.return_.expression
    e2 = e.arithmetic_operator.left
    e2.arithmetic_operator.left.atom.field.component.add().name = 'x'
    e2.arithmetic_operator.right.atom.literal.integer.value = 3
    e2.arithmetic_operator.operator = protocall_pb2.ArithmeticOperator.Op.Value("PLUS")
    e.arithmetic_operator.right.atom.literal.integer.value = 9
    e.arithmetic_operator.operator = protocall_pb2.ArithmeticOperator.Op.Value("MULTIPLY")

    return p

def test_execute():
    p = create_block()
    pr = Protocall()
    print "Program:"
    print dump.dump(p)
    result = pr.execute(p)
    print "Result:"
    print result
    return result

def create_conditional(c1, c2):
    p = protocall_pb2.Block()

    s = p.statement.add()

    e = s.conditional.if_scope.expression
    e.atom.literal.CopyFrom(c1)
    statement = s.conditional.if_scope.scope.block.statement.add()
    statement.return_.expression.atom.literal.integer.value = 10

    elif_expression_scope = s.conditional.elif_scope.add()
    elif_expression_scope.expression.atom.literal.CopyFrom(c2)
    statement = elif_expression_scope.scope.block.statement.add()
    statement.return_.expression.atom.literal.integer.value = 20

    statement = s.conditional.else_scope.block.statement.add()
    statement.return_.expression.atom.literal.integer.value = 30

    return p


def test_conditional(c1, c2):
    p = create_conditional(c1, c2)
    pr = Protocall()
    print "Program:"
    print dump.dump(p)
    result = pr.execute(p)
    print "Result:"
    print result
    return result

def create_conditional_expression(i1, i2, op):
    p = protocall_pb2.Block()

    s = p.statement.add()

    e = s.conditional.if_scope.expression
    e.comparison_operator.left.atom.literal.integer.value = i1
    e.comparison_operator.right.atom.literal.integer.value = i2
    e.comparison_operator.operator = protocall_pb2.ComparisonOperator.Op.Value(op)
    statement = s.conditional.if_scope.scope.block.statement.add()
    statement.return_.expression.atom.literal.integer.value = 10

    statement = s.conditional.else_scope.block.statement.add()
    statement.return_.expression.atom.literal.integer.value = 20

    return p

def test_conditional_expression(i1, i2, op):
    p = create_conditional_expression(i1, i2, op)
    pr = Protocall()
    print "Program:"
    print dump.dump(p)
    result = pr.execute(p)
    print "Result:"
    print result
    return result

def create_call():
    p = protocall_pb2.Block()

    s = p.statement.add()

    s.call.field.component.add().name = "print_"
    arg = s.call.argument.add()
    arg.identifier.name = 'x'
    arg.expression.atom.literal.integer.value = 5

    arg = s.call.argument.add()
    arg.identifier.name = 'y'
    arg.expression.atom.literal.integer.value = 7

    arg = s.call.argument.add()
    arg.identifier.name = 'z'
    arg.expression.atom.literal.integer.value = 7

    s = p.statement.add()
    s.call.field.component.add().name = "print_"

    s = p.statement.add()
    s.assignment.field.component.add().name = 'x'
    e = s.assignment.expression
    e.atom.literal.integer.value = 7

    s = p.statement.add()
    s.call.field.component.add().name = "print_"
    arg = s.call.argument.add()
    arg.identifier.name = 'x'
    e = arg.expression.atom.expression
    e.atom.field.component.add().name = 'x'

    s = p.statement.add()
    s.call.field.component.add().name = "print_"

    s = p.statement.add()
    s.call.field.component.add().name = "print_"
    arg = s.call.argument.add()
    arg.identifier.name = 'x'
    e = arg.expression.atom.expression
    e.arithmetic_operator.left.atom.field.component.add().name = 'x'
    e.arithmetic_operator.right.atom.literal.integer.value = 3
    e.arithmetic_operator.operator = protocall_pb2.ArithmeticOperator.Op.Value("PLUS")

    return p

def test_call():
    p = create_call()
    pr = Protocall()
    print "Program:"
    print dump.dump(p)
    result = pr.execute(p)
    print "Result:"
    print result
    return result

def create_call2():
    p = protocall_pb2.Block()

    s = p.statement.add()
    c = s.return_.expression.call
    c.field.component.add().name = "double"
    arg = c.argument.add()
    arg.identifier.name = 'x'
    arg.expression.atom.literal.integer.value = 3

    return p

def test_call2():
    p = create_call2()
    pr = Protocall()
    print "Program:"
    print dump.dump(p)
    result = pr.execute(p)
    print "Result:"
    print result
    return result

def create_call3():
    p = protocall_pb2.Block()

    s = p.statement.add()
    s.assignment.field.component.add().name = 'x'
    e = s.assignment.expression
    e.call.field.component.add().name = "double"
    arg = e.call.argument.add()
    arg.identifier.name = 'x'
    arg.expression.atom.literal.integer.value = 3

    s = p.statement.add()
    s.return_.expression.atom.field.component.add().name = 'x'

    return p

def test_call3():
    # This test fails when it's just a bare call() without a return().
    # The interpreter is supposed to return the return value of the last statement but it doesn't seem to.
    p = create_call3()
    pr = Protocall()
    print "Program:"
    print dump.dump(p)
    result = pr.execute(p)
    print "Result:"
    print result
    return result


def create_while():
    p = protocall_pb2.Block()

    s = p.statement.add()
    s.assignment.field.component.add().name = 'x'
    e = s.assignment.expression
    e.atom.literal.integer.value = 5

    s = p.statement.add()
    s.call.field.component.add().name = "print_"
    arg = s.call.argument.add()
    arg.identifier.name = 's'
    arg.expression.atom.literal.string.value = 'Start'

    s = p.statement.add()
    es = s.while_.expression_scope
    e = es.expression
    e.comparison_operator.left.atom.field.component.add().name = 'x'
    e.comparison_operator.right.atom.literal.integer.value = 0
    e.comparison_operator.operator = protocall_pb2.ComparisonOperator.Op.Value("GREATER_THAN")

    # Inside while loop
    s = es.scope.block.statement.add()
    s.call.field.component.add().name = "print_"
    arg = s.call.argument.add()
    arg.identifier.name = 'x'
    arg.expression.atom.field.component.add().name = 'x'

    s = es.scope.block.statement.add()
    s.assignment.field.component.add().name = 'x'
    e = s.assignment.expression
    e.arithmetic_operator.left.atom.field.component.add().name = 'x'
    e.arithmetic_operator.right.atom.literal.integer.value = 1
    e.arithmetic_operator.operator = protocall_pb2.ArithmeticOperator.Op.Value("MINUS")

    s = p.statement.add()
    s.call.field.component.add().name = "print_"
    arg = s.call.argument.add()
    arg.identifier.name = 's'
    arg.expression.atom.literal.string.value = 'Done'

    return p

def test_while():
    p = create_while()
    pr = Protocall()
    print "Program:"
    print dump.dump(p)
    result = pr.execute(p)
    print "Result:"
    print result
    return result

def create_define():
    p = protocall_pb2.Block()

    s = p.statement.add()
    s.define.field.component.add().name = "double_udf"
    b = s.define.scope.block

    # Inside function
    s = b.statement.add()
    e = s.return_.expression
    e.arithmetic_operator.left.atom.field.component.add().name = 'x'
    e.arithmetic_operator.right.atom.literal.integer.value = 2
    e.arithmetic_operator.operator = protocall_pb2.ArithmeticOperator.Op.Value("MULTIPLY")

    s = p.statement.add()
    s.call.field.component.add().name = "double_udf"
    arg = s.call.argument.add()
    arg.identifier.name = 'x'
    arg.expression.atom.literal.integer.value = 4

    return p

def test_define():
    p = create_define()
    pr = Protocall()
    print "Program:"
    print dump.dump(p)
    result = pr.execute(p)
    print "Result:"
    print result
    return result

def create_setq():
    p = protocall_pb2.Block()

    s = p.statement.add()
    s.call.field.component.add().name = 'setq'
    a = protocall_pb2.Atom()
    arg = s.call.argument.add()
    arg.identifier.name = 'arg0'
    arg.expression.atom.field.component.add().name = 'x'
    arg = s.call.argument.add()
    arg.identifier.name = 'arg1'
    arg.expression.atom.literal.integer.value = 5

    s = p.statement.add()
    s.call.field.component.add().name = "print_"
    arg = s.call.argument.add()
    arg.identifier.name = 'x'
    arg.expression.atom.field.component.add().name = 'x'

    return p

def create_program():
    p = protocall_pb2.Block()

    s = p.statement.add()
    s.assignment.field.component.add().name = 'x'
    e = s.assignment.expression
    e.atom.literal.integer.value = 5

    s = p.statement.add()
    s.call.field.component.add().name = "print_"
    arg = s.call.argument.add()
    arg.identifier.name = 's'
    arg.expression.atom.literal.string.value = 'Start'

    s = p.statement.add()
    es = s.while_.expression_scope
    e = es.expression
    e.comparison_operator.left.atom.field.component.add().name = 'x'
    e.comparison_operator.right.atom.literal.integer.value = 0
    e.comparison_operator.operator = protocall_pb2.ComparisonOperator.Op.Value("GREATER_THAN")

    # Inside while loop
    s = es.scope.block.statement.add()
    s.call.field.component.add().name = "print_"
    arg = s.call.argument.add()
    arg.identifier.name = 'x'
    arg.expression.atom.field.component.add().name = 'x'

    s = es.scope.block.statement.add()
    e = s.conditional.if_scope.expression
    e.comparison_operator.left.atom.field.component.add().name = 'x'
    e.comparison_operator.right.atom.literal.integer.value = 3
    e.comparison_operator.operator = protocall_pb2.ComparisonOperator.Op.Value("EQUALS")
    statement = s.conditional.if_scope.scope.block.statement.add()
    statement.call.field.component.add().name = "print_"
    arg = statement.call.argument.add()
    arg.identifier.name = 's'
    arg.expression.atom.literal.string.value = 'fizz'
    elif_expression_scope = s.conditional.elif_scope.add()
    e = elif_expression_scope.expression
    e.comparison_operator.left.atom.field.component.add().name = 'x'
    e.comparison_operator.right.atom.literal.integer.value = 2
    e.comparison_operator.operator = protocall_pb2.ComparisonOperator.Op.Value("EQUALS")
    statement = elif_expression_scope.scope.block.statement.add()
    statement.call.field.component.add().name = "print_"
    arg = statement.call.argument.add()
    arg.identifier.name = 's'
    arg.expression.atom.literal.string.value = 'fuzz'
    statement = s.conditional.else_scope.block.statement.add()
    statement.call.field.component.add().name = "print_"
    arg = statement.call.argument.add()
    arg.identifier.name = 's'
    arg.expression.atom.literal.string.value = 'buzz'

    s = es.scope.block.statement.add()
    s.assignment.field.component.add().name = 'x'
    e = s.assignment.expression
    e.arithmetic_operator.left.atom.field.component.add().name = 'x'
    e.arithmetic_operator.right.atom.literal.integer.value = 1
    e.arithmetic_operator.operator = protocall_pb2.ArithmeticOperator.Op.Value("MINUS")

    s = p.statement.add()
    s.call.field.component.add().name = "print_"
    arg = s.call.argument.add()
    arg.identifier.name = 's'
    arg.expression.atom.literal.string.value = 'Done'

    s = p.statement.add()
    v = s.return_.expression
    v.atom.field.component.add().name = 'x'

    return p

def test_program():
    p = create_program()
    pr = Protocall()
    print "Program:"
    print dump.dump(p)
    result = pr.execute(p)
    print "Result:"
    print result
    return result

def create_proto_expression():
    s= """arithmetic_operator { left { atom { field { component { name: "a" } component { name: "value" } } } } right { arithmetic_operator { left { atom { field { component { name: "xyz" } component { name: "value" } } } } right { atom { field { component { name: "b" } component { name: "value" } } } } operator: PLUS } } operator: MULTIPLY }"""

    e = protocall_pb2.Expression()
    text_format.Merge(s, e)
    return e


def test_evaluate_proto_expression():
    expression = create_proto_expression()
    a = protocall_pb2.Atom()
    p = a.literal.proto
    p.field.component.add().name = "Integer"
    p.value = "value: 9"
    b = protocall_pb2.Atom()
    p = b.literal.proto
    p.field.component.add().name = "Integer"
    p.value = "value: 5"
    xyz = protocall_pb2.Atom()
    p = xyz.literal.proto
    p.field.component.add().name = "Integer"
    p.value = "value: 5"
    symbols = Symbols({'a': a,
                       'b': b,
                       'xyz': xyz})
    pr = Protocall(symbols)
    result = pr.evaluate(expression)
    return result

class RuntimeTest(unittest.TestCase):

  def testEvaluate(self):
    assert test_evaluate().literal.integer.value == 90

  def testEvaluateArray(self):
    assert test_evaluate_array().literal.array.element[0].atom.literal.integer.value == 10

  def testExecute(self):
    assert test_execute().atom.literal.integer.value == 135

  def testConditional(self):
    assert test_conditional(literal_true, literal_false).atom.literal.integer.value == 10
    assert test_conditional(literal_false, literal_true).atom.literal.integer.value == 20
    assert test_conditional(literal_false, literal_false).atom.literal.integer.value == 30

  def testConditionalExpression(self):
    assert test_conditional_expression(1, 1, "LESS_THAN").atom.literal.integer.value == 20
    assert test_conditional_expression(1, 1, "EQUALS").atom.literal.integer.value == 10
    assert test_conditional_expression(1, 1, "GREATER_THAN").atom.literal.integer.value == 20
    assert test_conditional_expression(1, 2, "LESS_THAN").atom.literal.integer.value == 10
    assert test_conditional_expression(1, 2, "EQUALS").atom.literal.integer.value == 20
    assert test_conditional_expression(1, 2, "GREATER_THAN").atom.literal.integer.value == 20
    assert test_conditional_expression(2, 1, "LESS_THAN").atom.literal.integer.value == 20
    assert test_conditional_expression(2, 1, "EQUALS").atom.literal.integer.value == 20
    assert test_conditional_expression(2, 1, "GREATER_THAN").atom.literal.integer.value == 10

  def testCall(self):
    test_call()
    assert test_call2().atom.literal.integer.value == 6
    assert test_call3().atom.literal.integer.value == 6

  def testWhile(self):
    test_while()

  def testDefine(self):
    assert test_define().atom.literal.integer.value == 8

  def testProgram(self):
    assert test_program().atom.literal.integer.value == 0

  def testEvaluateProtoExpression(self):
    assert test_evaluate_proto_expression().literal.integer.value == 90


if __name__ == '__main__':
  unittest.main()
