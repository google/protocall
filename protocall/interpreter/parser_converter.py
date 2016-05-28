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

from pyparsing import ParseResults
from protocall.proto import protocall_pb2

from grammar import expression, statement, assignment, call, return_, block, scope, define, while_expression, while_scope, if_expression, if_scope, elif_expression, elif_scope, elif_scopes, else_scope, conditional
from AST import Call, Assignment, ArrayAssignment, Integer, String, Boolean, Proto, Array, Identifier, Field, ArrayRef, While, ArithmeticOperator, ComparisonOperator, Conditional, Return, Define

def convert_field(field):
  f = protocall_pb2.Field()
  for component in field.components:
    c = f.component.add()
    c.name = component.identifier
  return f

def convert_statement(statement):
    s = protocall_pb2.Statement()
    if isinstance(statement.statement, Call):
      call = statement.statement
      field, args = call.field, call.args
      c = protocall_pb2.Call()
      c.field.CopyFrom(convert_field(field))
      for arg in args:
        a = c.argument.add()
        a.identifier.name = arg.identifier.identifier
        a.expression.CopyFrom(convert_expression(arg.expression.expression))
      s.call.CopyFrom(c)
    elif isinstance(statement.statement, Assignment):
      assignment = statement.statement
      field, expression = assignment.field, assignment.expression
      a = protocall_pb2.Assignment()
      a.field.CopyFrom(convert_field(field))
      a.expression.CopyFrom(convert_expression(expression.expression))
      s.assignment.CopyFrom(a)
    elif isinstance(statement.statement, ArrayAssignment):
      array_assignment = statement.statement
      array_ref, expression = array_assignment.array_ref, array_assignment.expression
      a = protocall_pb2.ArrayAssignment()
      a.array_ref.field.CopyFrom(convert_field(array_ref.field))
      a.array_ref.index.value = array_ref.index
      a.expression.CopyFrom(convert_expression(expression.expression))
      s.array_assignment.CopyFrom(a)
    elif isinstance(statement.statement, While):
      while_expression = statement.statement
      expression, scope = while_expression.expression, while_expression.scope
      w = protocall_pb2.While()
      w.expression_scope.expression.CopyFrom(convert_expression(expression.expression))
      w.expression_scope.scope.CopyFrom(convert_scope(scope.scope))
      s.while_.CopyFrom(w)
    elif isinstance(statement.statement, Conditional):
      conditional = statement.statement
      if_scope = conditional.if_scope
      elif_scopes = conditional.elif_scopes
      c = protocall_pb2.Conditional()
      c.if_scope.expression.CopyFrom(convert_expression(if_scope.expression.expression))
      c.if_scope.scope.CopyFrom(convert_scope(if_scope.scope.scope))
      for elif_scope in elif_scopes:
        es = c.elif_scope.add()
        es.expression.CopyFrom(convert_expression(elif_scope.expression.expression))
        es.scope.CopyFrom(convert_scope(elif_scope.scope.scope))
      else_scope = conditional.else_scope
      if else_scope:
        c.else_scope.CopyFrom(convert_scope(else_scope.scope.scope))
      s.conditional.CopyFrom(c)
    elif isinstance(statement.statement, Return):
      return_ = statement.statement
      expression = return_.expression
      r = protocall_pb2.Return()
      r.expression.CopyFrom(convert_expression(expression.expression))
      s.return_.CopyFrom(r)
    elif isinstance(statement.statement, Define):
      define = statement.statement
      field = define.field
      scope = define.scope
      d = protocall_pb2.Define()
      d.field.CopyFrom(convert_field(field))
      d.scope.CopyFrom(convert_scope(scope.scope))
      s.define.CopyFrom(d)
    else:
      print statement.statement
      raise RuntimeError
    return s

def convert_block(block):
  bl = protocall_pb2.Block()
  for statement in block.block:
    s = convert_statement(statement)
    bl.statement.add().CopyFrom(s)
  return bl

def convert_argument(argument):
  ar = protocall_pb2.Argument()
  ar.identifier.name = argument.identifier.identifier
  e = convert_expression(argument.expression.expression)
  ar.expression.CopyFrom(e)
  return ar

def convert_scope(scope):
  s_pb = protocall_pb2.Scope()
  block = scope.block
  for statement in block:
    s_pb.block.statement.add().CopyFrom(convert_statement(statement))
  return s_pb

def convert_arithmetic_operator(arithmetic_operator, e):
  if arithmetic_operator.operator == '*':
    op = protocall_pb2.ArithmeticOperator.Op.Value("MULTIPLY")
  elif arithmetic_operator.operator == '/':
    op = protocall_pb2.ArithmeticOperator.Op.Value("DIVIDE")
  elif arithmetic_operator.operator == '+':
    op = protocall_pb2.ArithmeticOperator.Op.Value("PLUS")
  elif arithmetic_operator.operator == '-':
    op = protocall_pb2.ArithmeticOperator.Op.Value("MINUS")
  else:
    print arithmetic_operator.operator
    raise RuntimeError
  e.arithmetic_operator.operator = op
  left = convert_expression(arithmetic_operator.left)
  if isinstance(left, protocall_pb2.Expression):
    e.arithmetic_operator.left.CopyFrom(left)
  elif isinstance(left, protocall_pb2.Identifier):
    e.atom.identifier.CopyFrom(left)
  else:
    raise RuntimeError
  e.arithmetic_operator.left.CopyFrom(left)

  right = convert_expression(arithmetic_operator.right)
  if isinstance(right, protocall_pb2.Expression):
    e.arithmetic_operator.right.CopyFrom(right)
  elif isinstance(right, protocall_pb2.Identifier):
    e.atom.identifier.CopyFrom(right)
  else:
    raise RuntimeError
  e.arithmetic_operator.right.CopyFrom(right)

def convert_comparison_operator(comparison_operator, e):
  if comparison_operator.operator == '>':
    op = protocall_pb2.ComparisonOperator.Op.Value("GREATER_THAN")
  elif comparison_operator.operator == '<':
    op = protocall_pb2.ComparisonOperator.Op.Value("LESS_THAN")
  elif comparison_operator.operator == '==':
    op = protocall_pb2.ComparisonOperator.Op.Value("EQUALS")
  else:
    print comparison_operator.operator
    raise RuntimeError
  e.comparison_operator.operator = op
  left = convert_expression(comparison_operator.left)
  if isinstance(left, protocall_pb2.Expression):
    e.comparison_operator.left.CopyFrom(left)
  elif isinstance(left, protocall_pb2.Identifier):
    e.atom.identifier.CopyFrom(left)
  else:
    raise RuntimeError
  e.comparison_operator.left.CopyFrom(left)

  right = convert_expression(comparison_operator.right)
  if isinstance(right, protocall_pb2.Expression):
    e.comparison_operator.right.CopyFrom(right)
  elif isinstance(right, protocall_pb2.Identifier):
    e.atom.identifier.CopyFrom(right)
  else:
    raise RuntimeError
  e.comparison_operator.right.CopyFrom(right)

def convert_expression(expression):
  e = protocall_pb2.Expression()

  if isinstance(expression, Integer):
    e.atom.literal.integer.value = expression.value
  elif isinstance(expression, String):
    e.atom.literal.string.value = expression.value
  elif isinstance(expression, Boolean):
    e.atom.literal.boolean.value = expression.value
  elif isinstance(expression, Proto):
    e.atom.literal.proto.field.CopyFrom(convert_expression(expression.field).atom.field)
    e.atom.literal.proto.value = str(expression.proto)
  elif isinstance(expression, Field):
    e.atom.field.CopyFrom(convert_field(expression))
  elif isinstance(expression, Array):
    array = e.atom.literal.array
    for item in expression.elements:
      element = array.element.add()
      element.CopyFrom(convert_expression(item.expression))
  elif isinstance(expression, ArrayRef):
    e.atom.array_ref.field.CopyFrom(convert_field(expression.field))
    e.atom.array_ref.index.value = expression.index
  elif isinstance(expression, ArithmeticOperator):
    convert_arithmetic_operator(expression, e)
  elif isinstance(expression, ComparisonOperator):
    convert_comparison_operator(expression, e)
  elif isinstance(expression, Call):
    e.call.field.CopyFrom(convert_field(expression.field))
    for arg in expression.args:
      a = e.call.argument.add()
      a.CopyFrom(convert_argument(arg))
  else:
    print expression.__class__
    raise RuntimeError
  return e
