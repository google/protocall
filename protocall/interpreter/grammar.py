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
import copy
from pyparsing import nestedExpr, Forward, Word, alphas, nums, alphanums, oneOf, Literal, operatorPrecedence, opAssoc, infixNotation, Suppress, delimitedList, And, Group, OneOrMore, Optional, Or, ZeroOrMore, ParseResults, Keyword, dblQuotedString, cStyleComment, pythonStyleComment
from AST import Identifier, Field, ArrayRef, Integer, String, Boolean, Proto, Array, SignOperator, ArithmeticOperator, ComparisonOperator, Expression, Assignment, ArrayAssignment, Call, Return, Define, IfScope, ElifScope, ElifScopes, ElseScope, Conditional, While, Statement, Block, Scope
from protocall.proto.text_format_parser import text_format_parser

def identifier_fn(s,l,t):
  return Identifier(t[0])
def field_fn(s,l,t):
  return Field(t)
def array_ref_fn(s,l,t):
  return ArrayRef(t[0], int(t[1]))
def integer_fn(s,l,t):
  return Integer(int(t[0]))
def string_fn(s,l,t):
  return String(t[0][1:-1])
def array_fn(s,l,t):
  return Array(t[0])
def boolean_fn(s,l,t):
  return Boolean(bool(t[0] == 'true'))
def proto_fn(s,l,t):
  return Proto(t[0], t[1])
def signop_fn(s,l,t):
  return SignOperator(*t[0])
def binop_fn(s,l,t):
  return ArithmeticOperator(*t[0])
def comparison_operator_fn(s,l,t):
  return ComparisonOperator(*t[0])
def expression_fn(s,l,t):
  return Expression(t[0])
def assignment_fn(s,l,t):
  return Assignment(*t)
def array_assignment_fn(s,l,t):
  return ArrayAssignment(t[0], t[1])
def call_fn(s,l,t):
  return Call(t[0], t[1])
def return_fn(s,l,t):
  return Return(t[0])
def define_fn(s,l,t):
  return Define(t[0], t[1])
def if_scope_fn(s,l,t):
  return IfScope(*t)
def elif_scope_fn(s,l,t):
  return ElifScope(*t)
def elif_scopes_fn(s,l,t):
  return ElifScopes(t)
def else_scope_fn(s,l,t):
  return ElseScope(t[0])
def conditional_fn(s,l,t):
  return Conditional(t)
def while_scope_fn(s,l,t):
  return While(t[0], t[1])
def statement_fn(s,l,t):
  return Statement(t[0])
def block_fn(s,l,t):
  return Block(t)
def scope_fn(s,l,t):
  return Scope(t[0][0])


if_ = Keyword("if")
elif_ = Keyword("elif")
else_ = Keyword("else")
return_ = Keyword("return")
define = Keyword("define")
while_ = Keyword("while")
true = Keyword("true")
false = Keyword("false")
any_keyword = if_ | elif_ | else_ | return_ | define | while_ | true | false

identifier = Word(alphas+'_',alphanums+"_")
identifier.setParseAction(identifier_fn)
identifier.ignore(any_keyword)
field = delimitedList(identifier, '.')
field.setParseAction(field_fn)
array_ref = field + Suppress('[') + Word(nums) + Suppress(']')
array_ref.setParseAction(array_ref_fn)
integer = Word(nums)
integer.setParseAction(integer_fn)
string = copy.copy(dblQuotedString)
string.setParseAction(string_fn)
boolean = (true | false)
boolean.setParseAction(boolean_fn)
proto = field + Suppress('<') + text_format_parser.parser + Suppress('>')
proto.setParseAction(proto_fn)

call = Forward()
literal = (integer | string | boolean | proto)
operand = (literal | call | array_ref | field)


multop = Word('*')
divop = Word('/')
plusop = Word('+')
minusop = Word('-')
signop = oneOf('- +')
operation = infixNotation( operand, [
    (signop, 2, opAssoc.LEFT, binop_fn),
    (multop, 2, opAssoc.LEFT, binop_fn),
    (divop, 2, opAssoc.LEFT, binop_fn),
    (plusop, 2, opAssoc.LEFT, binop_fn),
    (minusop, 2, opAssoc.LEFT, binop_fn),
])


comparisonop = oneOf('< > ==')

comparison_operation = infixNotation( operation, [
    (comparisonop, 2, opAssoc.LEFT, comparison_operator_fn)
])("comparison_operation")

array = Forward()
expression = (comparison_operation | operation | operand | array)
expression.setParseAction(expression_fn)
array << Suppress('{') + Group(delimitedList(expression)) + Suppress('}')
array.setParseAction(array_fn)

assignment = field + Suppress('=') + expression
assignment.setParseAction(assignment_fn)
array_assignment = array_ref + Suppress('=') + expression
array_assignment.setParseAction(array_assignment_fn)
args = Group(Optional(delimitedList(Group(identifier + Suppress(Literal('=')) + expression))))
call << (field + Suppress(Literal('(')) + args + Suppress(Literal(')')))
call.setParseAction(call_fn)
return_expression = (Suppress(return_) + expression)
return_expression.setParseAction(return_fn)

scope = Forward()

define_function_scope = (Suppress(define) + field + scope)
define_function_scope.setParseAction(define_fn)
if_expression = (Suppress(if_) + Suppress(Literal('(')) + expression + Suppress(Literal(')')))
if_scope = (if_expression + scope)
if_scope.setParseAction(if_scope_fn)
elif_expression = (Suppress(elif_) + Suppress(Literal('(')) + expression + Suppress(Literal(')')))
elif_scope = (elif_expression + scope)
elif_scope.setParseAction(elif_scope_fn)
elif_scopes = ZeroOrMore(Group(elif_scope))
elif_scopes.setParseAction(elif_scopes_fn)
else_scope = (Suppress(else_) + scope)
else_scope.setParseAction(else_scope_fn)
conditional = (if_scope + Optional(elif_scopes) + Optional(else_scope))
conditional.setParseAction(conditional_fn)

while_expression = (Suppress(while_) + Suppress(Literal('(')) + expression + Suppress(Literal(')')))
while_scope = (while_expression + scope)
while_scope.setParseAction(while_scope_fn)

statement = ((array_assignment | assignment | conditional | call | return_expression | while_scope | define_function_scope) + Suppress(';'))
statement.setParseAction(statement_fn)

block = OneOrMore((statement | cStyleComment | pythonStyleComment))
block.setParseAction(block_fn)
block.ignore(cStyleComment)
block.ignore(pythonStyleComment)

scope << (Suppress(Literal('{')) + Group(block) + Suppress(Literal('}')))
scope.setParseAction(scope_fn)
