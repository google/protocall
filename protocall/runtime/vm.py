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
import sys
import types
from protocall.proto import protocall_pb2
from google.protobuf import text_format
import subrs
import builtins
from truth import is_true
from symbols import Symbols
from operators import arithmetic_operators, comparison_operators

class Protocall:
  def __init__(self, symbols=None, tracing=False):
    if symbols is not None:
      self.symbols = symbols
    else:
      self.symbols = Symbols()
    self.subrs = dict([(name, getattr(subrs, name)) for name in dir(subrs) if not name.startswith("_")])
    self.builtins = dict([(name, getattr(builtins, name)) for name in dir(builtins) if not name.startswith("_")])
    self.udfs = {}
    self.tracing = tracing

  def enable_tracing(self):
    self.tracing = True
  def disable_tracing(self):
    self.tracing = False

  def execute(self, block):
    for statement in block.statement:
      print "statement:", statement
      if self.tracing:
        print "hit ENTER for statement:"
        print text_format.MessageToString(statement, as_one_line=True)
        print "with local variables:",
        print self.symbols.locals()
        line = sys.stdin.readline().strip()
      try:
        if statement.HasField("assignment"):
          result = self.assignment(statement)
        elif statement.HasField("array_assignment"):
          result = self.array_assignment(statement)
        elif statement.HasField("call"):
          result = self.invoke(statement.call)
        elif statement.HasField("conditional"):
          e_result = self.evaluate(statement.conditional.if_scope.expression)
          if is_true(e_result):
            result = self.execute(statement.conditional.if_scope.scope.block)
          else:
            for expression_scope in statement.conditional.elif_scope:
              e_result = self.evaluate(expression_scope.expression)
              if is_true(e_result):
                result = self.execute(expression_scope.scope.block)
                break
            else:
              if len(statement.conditional.else_scope.block.statement):
                result = self.execute(statement.conditional.else_scope.block)
        elif statement.HasField("return_"):
          e_result = self.evaluate(statement.return_.expression)
          if isinstance(e_result, protocall_pb2.Expression):
            result = e_result
          elif isinstance(e_result, protocall_pb2.Atom):
            result = protocall_pb2.Expression()
            result.atom.CopyFrom(e_result)
          elif isinstance(e_result, protocall_pb2.Array):
            result = protocall_pb2.Expression()
            result.atom.CopyFrom(e_result)
          elif isinstance(e_result, int):
            result = protocall_pb2.Expression()
            result.atom.literal.integer.value = e_result
          elif isinstance(e_result, str):
            result = protocall_pb2.Expression()
            result.atom.literal.string.value = e_result
          else:
            print e_result.__class__
            raise RuntimeError
          ## Should call return here
        elif statement.HasField("while_"):
          while True:
            e_result = self.evaluate(statement.while_.expression_scope.expression)
            if is_true(e_result):
              self.execute(statement.while_.expression_scope.scope.block)
            else:
              break
          result = None
        elif statement.HasField("define"):
          ## Only support definition of top-level fields
          identifier = statement.define.field.component[0].name
          self.udfs[identifier] = statement.define.scope.block
          result = None
        else:
          raise RuntimeError(str(statement))
      except Exception as e:
        print "Execution failed at line:"
        print text_format.MessageToString(statement, as_one_line=True)
        import pdb; pdb.set_trace()
        print "foo"
    return result

  def handle_atom(self, atom):
    if atom.HasField("literal"):
      result = atom
    elif atom.HasField("expression"):
      result = self.evaluate(atom.expression)
    elif atom.HasField("field"):
      result = self.symbols.lookup_local(atom.field)
    elif atom.HasField("array_ref"):
      array = self.symbols.lookup_local(atom.array_ref.field)
      result = self.evaluate(array.element[atom.array_ref.index.value])
    else:
      raise RuntimeError
    return result

  def evaluate(self, expression):
    result = None
    assert isinstance(expression, protocall_pb2.Expression), type(expression)
    if expression.HasField("atom"):
      if expression.atom.literal.HasField("array"):
        for element in expression.atom.literal.array.element:
          e = protocall_pb2.Expression()
          e.atom.CopyFrom(self.evaluate(element))
          element.CopyFrom(e)
        result = expression.atom
      else:
        result = self.handle_atom(expression.atom)
    elif expression.HasField("call"):
      result = self.invoke(expression.call)
    elif expression.HasField("arithmetic_operator"):
      print "evaluate arithmetic operator"
      print "left before=", expression.arithmetic_operator.left
      print "right before=", expression.arithmetic_operator.right
      left = self.evaluate(expression.arithmetic_operator.left)
      right = self.evaluate(expression.arithmetic_operator.right)
      print "left=", left
      print "right=", right
      r = arithmetic_operators[expression.arithmetic_operator.operator](left, right)
      result = protocall_pb2.Atom()
      result.literal.CopyFrom(r)
    elif expression.HasField("comparison_operator"):
      left = self.evaluate(expression.comparison_operator.left)
      right = self.evaluate(expression.comparison_operator.right)
      r = comparison_operators[expression.comparison_operator.operator](left, right)
      result = protocall_pb2.Atom()
      result.literal.CopyFrom(r)
    else:
      raise RuntimeError
      import pdb; pdb.set_trace()
      print "expression:", expression
    return result

  def invoke(self, call):
    # For now, only support fields with a single component
    assert (len(call.field.component) == 1)
    name = call.field.component[0].name
    if name in self.subrs:
      function = self.subrs[name]
      result = function(self, call.argument, self.symbols)
    elif name in self.builtins or name in self.udfs:
      if name in self.builtins:
        function = self.builtins[name]
      elif name in self.udfs:
        function = self.udfs[name]
      else:
        raise RuntimeError
      args = [ (arg.identifier.name, self.evaluate(arg.expression)) for arg in call.argument ]
      self.symbols.push_frame()
      for arg in args:
        f = protocall_pb2.Field()
        f.component.add().name = arg[0]
        self.symbols.add_local_symbol(f, arg[1])
      if type(function) == types.FunctionType:
        result = function(args, self.symbols)
      elif isinstance(function, protocall_pb2.Block):
        result = self.execute(function)
      self.symbols.pop_frame()
    else:
      raise KeyError, name

    return result

  def assignment(self, a):
    print "assignment:", a
    e = self.evaluate(a.assignment.expression)
    if isinstance(e, protocall_pb2.Expression):
      e = e.atom
    if isinstance(e, protocall_pb2.Atom):
      if e.HasField("literal"):
        if e.literal.HasField("integer"):
          v = e.literal.integer.value
        elif e.literal.HasField("string"):
          v = e.literal.string.value
        elif e.literal.HasField("array"):
          v = e.literal.array
        elif e.literal.HasField("proto"):
          v = e
        else:
          raise RuntimeError
      else:
        raise RuntimeError
    else:
      raise RuntimeError
    self.symbols.add_local_symbol(a.assignment.field, v)
    return v

  def array_assignment(self, a):
    e = self.evaluate(a.array_assignment.expression)
    n = self.symbols.lookup(a.array_assignment.array_ref.field)
    x = a.array_assignment.array_ref.index.value
    n.element[a.array_assignment.array_ref.index.value].atom.CopyFrom(e)
    self.symbols.add_local_symbol(a.array_assignment.array_ref.field, e)
    return e
