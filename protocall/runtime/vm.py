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
          else:
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
          self.udfs[statement.define.identifier.name] = statement.define.scope.block
          result = None
        else:
          raise RuntimeError(str(statement))
      except Exception as e:
        print "Execution failed at line:"
        print text_format.MessageToString(statement, as_one_line=True)
        raise
    return result

  def handle_atom(self, atom):
    if atom.HasField("literal"):
      result = atom
    elif atom.HasField("expression"):
      result = self.evaluate(atom.expression)
    elif atom.HasField("identifier"):
      result = self.symbols.lookup_local(atom.identifier.name)
    elif atom.HasField("array_ref"):
      array = self.symbols.lookup_local(atom.array_ref.identifier.name).literal.array
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
      left = self.evaluate(expression.arithmetic_operator.left)
      right = self.evaluate(expression.arithmetic_operator.right)
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
    return result

  def invoke(self, call):
    if call.identifier.name in self.subrs:
      function = self.subrs[call.identifier.name]
      result = function(self, call.argument, self.symbols)
    elif call.identifier.name in self.builtins or call.identifier.name in self.udfs:
      if call.identifier.name in self.builtins:
        function = self.builtins[call.identifier.name]
      elif call.identifier.name in self.udfs:
        function = self.udfs[call.identifier.name]
      else:
        raise RuntimeError
      args = [ (arg.identifier.name, self.evaluate(arg.expression)) for arg in call.argument ]
      self.symbols.push_frame()
      for arg in args:
        self.symbols.add_local_symbol(arg[0], arg[1])
      if type(function) == types.FunctionType:
        result = function(args, self.symbols)
      elif isinstance(function, protocall_pb2.Block):
        result = self.execute(function)
      self.symbols.pop_frame()
    else:
      raise KeyError, call.identifier.name

    return result

  def assignment(self, a):
    e = self.evaluate(a.assignment.expression)
    self.symbols.add_local_symbol(a.assignment.identifier.name, e)
    return e

  def array_assignment(self, a):
    e = self.evaluate(a.array_assignment.expression)
    n = self.symbols.lookup(a.array_assignment.array_ref.identifier.name)
    x = a.array_assignment.array_ref.index.value
    n.literal.array.element[a.array_assignment.array_ref.index.value].atom.CopyFrom(e)
    self.symbols.add_local_symbol(a.assignment.identifier.name, e)
    return e
