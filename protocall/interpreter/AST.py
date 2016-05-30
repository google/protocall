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


class Identifier:
  def __init__(self, identifier):
    self.identifier = identifier

  def __getitem__(self, item):
    if item == 0:
      return self.identifier
    else:
      raise IndexError

  def __repr__(self):
    return self.identifier

class Field:
  def __init__(self, components):
    self.components = components

  def __getitem__(self, item):
    if item == 0:
      return self.components
    else:
      raise IndexError

  def __repr__(self):
    return ".".join([str(component) for component in self.components])

class ArrayRef:
  def __init__(self, field, index):
    self.field = field
    self.index = index

  def __getitem__(self, item):
    if item == 0:
      return self.field
    if item == 0:
      return self.index
    else:
      raise IndexError

  def __repr__(self):
    return self.field.field + "[" + str(self.index) + "]"

class Integer:
  def __init__(self, value):
    self.value = value

  def __getitem__(self, item):
    if item == 0:
      return self.value
    else:
      raise IndexError

  def __repr__(self):
    return str(self.value)

class String:
  def __init__(self, value):
    self.value = value

  def __getitem__(self, item):
    if item == 0:
      return self.value
    else:
      raise IndexError

  def __repr__(self):
    return self.value

class Boolean:
  def __init__(self, value):
    self.value = value

  def __getitem__(self, item):
    if item == 0:
      return self.value
    else:
      raise IndexError

  def __repr__(self):
    return str(self.value)

class Proto:
  def __init__(self, field, proto):
    self.field = field
    self.proto = proto

  def __getitem__(self, item):
    if item == 0:
      return self.field
    elif item == 1:
      return self.proto
    else:
      raise IndexError

  def __repr__(self):
    return "%s<%s>" % (self.field, str(self.proto))

class Array:
  def __init__(self, elements):
    self.elements = []
    for element in elements:
      self.elements.append(element)

  def __getitem__(self, item):
    return self.elements[item]

  def __repr__(self):
    return "{" + [element for element in elements] + "}"

class SignOperator:
  def __init__(self, operator, value):
    self.operator = operator
    self.value = value

  def __getitem__(self, item):
    if item == 0:
      return self.operator
    elif item == 1:
      return self.value
    else:
      raise IndexError

  def __repr__(self):
    return "%s%s" % (self.operator, repr(self.value))

class ArithmeticOperator:
  def __init__(self, left, operator, right):
    self.left = left
    self.operator = operator
    self.right = right

  def __getitem__(self, item):
    if item == 0:
      return self.left
    elif item == 1:
      return self.operator
    elif item == 2:
      return self.right
    else:
      raise IndexError

  def __repr__(self):
    return "(%s %s %s)" % (repr(self.left), self.operator, repr(self.right))

class ComparisonOperator:
  def __init__(self, left, operator, right):
    self.left = left
    self.operator = operator
    self.right = right

  def __getitem__(self, item):
    if item == 0:
      return self.left
    elif item == 1:
      return self.operator
    elif item == 2:
      return self.right
    else:
      raise IndexError

  def __repr__(self):
    return "(%s %s %s)" % (repr(self.left), self.operator, repr(self.right))


class Expression:
  def __init__(self, expression):
    self.expression = expression

  def __getitem__(self, item):
    return self.expression[item]

  def __repr__(self):
    return str(self.expression)


class Assignment:
  def __init__(self, field, expression):
    self.field = field
    self.expression = expression

  def __getitem__(self, item):
    if item == 0:
      return self.field
    elif item == 1:
      return self.expression
    else:
      raise IndexError

  def __repr__(self):
    return "%s = %s" % (self.field, repr(self.expression))

class ArrayAssignment:
  def __init__(self, array_ref, expression):
    self.array_ref = array_ref
    self.expression = expression

  def __getitem__(self, item):
    if item == 0:
      return self.array_ref
    elif item == 1:
      return self.expression
    else:
      raise IndexError

  def __repr__(self):
    return "%s = %s" % (self.array_ref, repr(self.expression))


class Argument:
  def __init__(self, identifier, expression):
    self.identifier = identifier
    self.expression = expression

  def __getitem__(self, item):
    if item == 0:
      return self.identifier
    elif item == 1:
      return self.expression
    else:
      raise IndexError

  def __repr__(self):
    return "%s = %s" % (self.identifier, repr(self.expression))

class Call:
  def __init__(self, field, args):
    self.field = field
    self.args = [Argument(arg[0], arg[1]) for arg in args]

  def __getitem__(self, item):
    if item == 0:
      return self.field
    elif item == 1:
      return self.args
    else:
      raise IndexError

  def __repr__(self):
    return "%s(%s)" % (self.field, ",".join([repr(arg) for arg in self.args]))


class Return:
  def __init__(self, expression):
    self.expression = expression

  def __getitem__(self, item):
    if item == 0:
      return self.expression
    else:
      raise IndexError

  def __repr__(self):
    return "return %s" % repr(self.expression)

class Define:
  def __init__(self, field, scope):
    self.field = field
    self.scope = scope

  def __getitem__(self, item):
    if item == 0:
      return self.field
    elif item == 1:
      return self.scope
    else:
      raise IndexError

  def __repr__(self):
    return "define %s %s" % (self.field, self.scope)


class IfScope:
  def __init__(self, expression, scope):
    self.expression = expression
    self.scope = scope

  def __getitem__(self, item):
    if item == 0:
      return self.expression
    elif item == 1:
      return self.scope

  def __repr__(self):
    return "if (%s) %s" % (self.expression, self.scope)


class ElifScope:
  def __init__(self, expression, scope):
    self.expression = expression
    self.scope = scope

  def __getitem__(self, item):
    if item == 0:
      return self.expression
    elif item == 1:
      return self.scope
    else:
      raise IndexError

  def __repr__(self):
    return "elif (%s) %s" % (self.expression, self.scope)


class ElifScopes:
  def __init__(self, scopes):
    self.scopes = [scope[0] for scope in scopes]

  def __getitem__(self, item):
    return self.scopes[item]

  def __repr__(self):
    return "%s" % (" ".join([repr(scope) for scope in self.scopes]))


class ElseScope:
  def __init__(self, scope):
    self.scope = scope

  def __getitem__(self, item):
    if item == 0:
      return self.scope
    else:
      raise IndexError

  def __repr__(self):
    return "else %s" % (self.scope)


class Conditional:
  def __init__(self, conditional):
    if_scope = conditional[0]
    elif_scopes = None
    else_scope = None
    if len(conditional) > 1:
      elif_scopes = conditional[1]
    if len(conditional) > 2:
      else_scope = conditional[2]
    self.if_scope = if_scope
    self.elif_scopes = elif_scopes
    self.else_scope = else_scope

  def __getitem__(self, item):
    if item == 0:
      return self.if_scope
    elif item == 1:
      return self.elif_scopes
    elif item == 2:
      return self.else_scopes
    else:
      raise IndexError

  def __repr__(self):
    result = [repr(self.if_scope)]
    if self.elif_scopes:
      result.append(repr(self.elif_scopes))
    if self.else_scope:
      result.append(repr(self.else_scope))
    return " ".join(result)


class While:
  def __init__(self, expression, scope):
    self.expression = expression
    self.scope = scope

  def __getitem__(self, item):
    if item == 0:
      return self.expression
    elif item == 1:
      return self.scope
    else:
      raise IndexError

  def __repr__(self):
    return "while (%s) %s" % (self.expression, self.scope)


class Statement:
  def __init__(self, statement):
    self.statement = statement

  def __getitem__(self, item):
    if item == 0:
      return self.statement
    else:
      raise IndexError

  def __repr__(self):
    return "%s;" % (self.statement)


class Block:
  def __init__(self, block):
    self.block = block

  def __getitem__(self, item):
    if item == 0:
      return self.block
    else:
      raise IndexError

  def __repr__(self):
    return " ".join([repr(statement) for statement in self.block])


class Scope:
  def __init__(self, scope):
    self.scope = scope

  def __getitem__(self, item):
    if item == 0:
      return self.scope
    else:
      raise IndexError

  def __repr__(self):
    return "{ %s }" % (repr(self.scope))

# Proto-specific AST:

class ProtoInteger:
  def __init__(self, value):
    self.value = value

  def __getitem__(self, item):
    if item == 0:
      return self.value
    else:
      raise IndexError

  def __repr__(self):
    return str(self.value)

class ProtoString:
  def __init__(self, value):
    self.value = value

  def __getitem__(self, item):
    if item == 0:
      return self.value
    else:
      raise IndexError

  def __repr__(self):
    return self.value

class ProtoData:
  def __init__(self, value):
    self.value = value

  def __getitem__(self, item):
    if item == 0:
      return self.value
    else:
      raise IndexError

  def __repr__(self):
    return str(self.value)

class TopLevelProtoDefinition:
  def __init__(self, identifier, data):
    self.identifier = identifier
    self.data = data

  def __getitem__(self, item):
    if item == 0:
      return self.identifier
    elif item == 1:
      return self.data
    else:
      raise IndexError

  def __repr__(self):
    return "%s: %s" % (self.identifier, self.data)

class NestedProto:
  def __init__(self, identifier, parser):
    self.identifier = identifier
    self.parser = parser

  def __getitem__(self, item):
    if item == 0:
      return self.identifier
    if item == 1:
      return self.parser
    else:
      raise IndexError

  def __repr__(self):
    return "%s { %s }" % (self.identifier, self.parser)

class ProtoParser:
  def __init__(self, values):
    self.values = values

  def __getitem__(self, item):
    if item == 0:
      return self.values
    else:
      raise IndexError

  def __repr__(self):
    return " ".join(["%s" % value for value in self.values])
